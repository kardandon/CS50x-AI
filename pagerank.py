import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    props = dict()
    count = len(corpus[page])
    for key in corpus.keys():
        if key in corpus[page]:
            props[key] = damping_factor / count
        else:
            props[key] = 0
        props[key] += (1 - damping_factor) / len(corpus.keys())
    return props
        
    
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    samples = []
    rank = dict()
    for a in corpus.keys():
        rank[a] = 0
    samples.append(random.choice(list(corpus.keys())))
    rank[samples[-1]] = 1
    for i in range(n-1):
        props = transition_model(corpus, samples[-1], damping_factor)
        rand = random.random()
        s = 0
        for key in props.keys():
            s += props[key]
            if s >= rand:
                samples.append(key)
                try:
                    rank[key] += 1
                except:
                    rank[key] = 1
                break
    for key in rank.keys():
        rank[key] /= n
    return rank
    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = dict()
    N = len(corpus.keys())
    
    for page in corpus:
        rank[page] = 1 / N

    flag = True
    while flag:
        flag = False
        dist = rank.copy()
        for page in corpus:
            rank[page] = (1 - damping_factor) / N
            for key in dist:
                if page not in corpus[key]:
                    continue
                x = len(corpus[key])
                if x == 0:
                    x = 1
                rank[page] += damping_factor * dist[key] / x
            flag = flag or abs(dist[page] - rank[page]) > 0.001
    return rank


if __name__ == "__main__":
    main()
