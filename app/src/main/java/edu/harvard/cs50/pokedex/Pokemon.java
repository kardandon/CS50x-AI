package edu.harvard.cs50.pokedex;

public class Pokemon {
    private String name;
    private String url;
    private String image_url;
    private int id;


    Pokemon(String name, String url, String image_url, int id) {
        this.name = name;
        this.url = url;
        this.image_url = image_url;
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public String getUrl() {
        return url;
    }
    public String getImage_url() {
        return image_url;
    }
    public int getId(){return id;}
}
