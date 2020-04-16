// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>
#include <string.h>
#include "dictionary.h"
#include <ctype.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;
// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

int count[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    node *tmp = NULL;
    tmp = table[hash(word)];
    while (tmp != NULL)
    {
        if (!strcasecmp(word, tmp->word))
        {
            return true;
        }
        tmp = tmp->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    node *tmp = NULL;
    bool flag = true;
    int cnt = 0;
    char temp[LENGTH + 1] = "";
    // TODO
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }
    while (!feof(dict))
    {
        cnt = 0;
        fscanf(dict, " %s ", temp);
        if (table[hash(temp)] == NULL)
        {
            table[hash(temp)] = (node *) malloc(sizeof(node));
            table[hash(temp)]->next  = NULL;
            strcpy(table[hash(temp)]->word, "");
        }
        tmp = table[hash(temp)];

        while (tmp->next != NULL)
        {
            cnt++;
            tmp = tmp->next;
        }
        tmp->next = (node *) malloc(sizeof(node));
        tmp->next->next = NULL;
        strcpy(tmp->next->word, "");
        strcpy(tmp->word, temp);
        cnt++;
        count[hash(temp)] = cnt;
    }
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    int a = 0;
    for (int i = 0 ; i < 26 ; i++)
    {
        a += count[i];
    }
    return a;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    node *tmp1 = NULL, *tmp2 = NULL;
    for (int i = 0 ; i < 26 ; i ++)
    {
        tmp1 = table[i];
        tmp2 = table[i];
        while (tmp1 != NULL)
        {
            tmp2 = tmp1->next;
            free(tmp1);
            tmp1 = tmp2;
        }
    }
    return true;
}
