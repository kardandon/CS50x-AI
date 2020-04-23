package edu.harvard.cs50.pokedex;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.ImageRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.InputStream;

public class PokemonActivity extends AppCompatActivity {
    private TextView nameTextView;
    private TextView numberTextView;
    private TextView type1TextView;
    private TextView type2TextView;
    private TextView infoView;
    private ImageView imageview;
    private String url;
    private String image_url;
    private RequestQueue requestQueue;
    private Button catchbutton;
    public boolean cought;
    public int id;
    private String textid;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pokemon);

        requestQueue = Volley.newRequestQueue(getApplicationContext());
        url = getIntent().getStringExtra("url");
        id = getIntent().getIntExtra("id",0);
        textid = Integer.toString(id);
        image_url = getIntent().getStringExtra("image_url");
        imageview = findViewById(R.id.pokemon_image);
        Bitmap bMap = BitmapFactory.decodeResource(getResources(), R.drawable.pokeball);
        imageview.setImageBitmap(bMap);
        nameTextView = findViewById(R.id.pokemon_name);
        numberTextView = findViewById(R.id.pokemon_number);
        type1TextView = findViewById(R.id.pokemon_type1);
        type2TextView = findViewById(R.id.pokemon_type2);
        catchbutton = findViewById(R.id.catch_button);
        infoView = findViewById(R.id.poke_info);

        load();
    }
    public void load() {
        new DownloadImageTask(imageview).execute(image_url);
        type1TextView.setText("");
        type2TextView.setText("");
        int a;
        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                try {
                    String name = response.getString("name");
                    name = name.substring(0,1).toUpperCase() + name.substring(1);
                    nameTextView.setText(name);
                    numberTextView.setText(String.format("#%03d", id));
                    cought = getPreferences(Context.MODE_PRIVATE).getBoolean(textid,cought);
                    if (cought){
                        catchbutton.setText("Release");
                    }
                    else {
                        catchbutton.setText("Catch");
                    }

                    JSONArray typeEntries = response.getJSONArray("types");
                    for (int i = 0; i < typeEntries.length(); i++) {
                        JSONObject typeEntry = typeEntries.getJSONObject(i);
                        int slot = typeEntry.getInt("slot");
                        String type = typeEntry.getJSONObject("type").getString("name");
                        type = type.substring(0,1).toUpperCase() + type.substring(1);

                        if (slot == 1) {
                            type1TextView.setText(type);
                        }
                        else if (slot == 2) {
                            type2TextView.setText(type);
                        }
                    }
                } catch (JSONException e) {
                    Log.e("cs50", "Pokemon json error", e);
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.e("cs50", "Pokemon details error", error);
            }
        });
        requestQueue.add(request);
        String url2 =  "https://pokeapi.co/api/v2/pokemon-species/" + textid;
        request = new JsonObjectRequest(Request.Method.GET, url2, null, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                String text = "";
                try {
                    JSONArray typeEntries = response.getJSONArray("flavor_text_entries");
                    for (int i = 0; i < typeEntries.length(); i++) {
                        JSONObject typeEntry = typeEntries.getJSONObject(i);
                        if (typeEntry.getJSONObject("language").getString("name").equals("en")){
                            text = typeEntry.getString("flavor_text");
                            break;
                        }
                    }
                    infoView.setText(text);
                } catch (JSONException e) {
                    Log.e("cs50", "Pokemon json error", e);
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.e("cs50", "Pokemon details error", error);
            }
        });

        requestQueue.add(request);
    }
    private class DownloadImageTask extends AsyncTask<String, Void, Bitmap> {
        ImageView bmImage;

        public DownloadImageTask(ImageView bmImage) {
            this.bmImage = bmImage;
        }

        protected Bitmap doInBackground(String... urls) {
            String urldisplay = urls[0];
            Bitmap mIcon11 = null;
            try {
                InputStream in = new java.net.URL(urldisplay).openStream();
                mIcon11 = BitmapFactory.decodeStream(in);
            } catch (Exception e) {
                Log.e("Error", e.getMessage());
                e.printStackTrace();
            }
            return mIcon11;
        }
        protected void onPostExecute(Bitmap result) {
            bmImage.setImageBitmap(result);
        }
    }
    public void toggleCatch(View view) {
        Button catchbutton = view.findViewById(R.id.catch_button);
       cought = !cought;
        getPreferences(Context.MODE_PRIVATE).edit().putBoolean(textid,cought).commit();
        if (cought) {
            catchbutton.setText("Release");
        } else {
            catchbutton.setText("Catch");
        }
    }
}
