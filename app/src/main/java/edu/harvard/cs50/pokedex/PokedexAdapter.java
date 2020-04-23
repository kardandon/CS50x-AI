package edu.harvard.cs50.pokedex;

import android.content.Context;
import android.content.Intent;
import android.os.Parcel;
import android.os.Parcelable;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Filter;
import android.widget.Filterable;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class PokedexAdapter extends RecyclerView.Adapter<PokedexAdapter.PokedexViewHolder> implements Filterable {
    public class PokedexViewHolder extends RecyclerView.ViewHolder {
        public LinearLayout containerView;
        public TextView textView;


        PokedexViewHolder(View view) {
            super(view);

            containerView = view.findViewById(R.id.pokedex_row);
            textView = view.findViewById(R.id.pokedex_row_text_view);

            containerView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Pokemon current = (Pokemon) containerView.getTag();
                    Intent intent = new Intent(v.getContext(), PokemonActivity.class);
                    intent.putExtra("url", current.getUrl());
                    intent.putExtra("id", current.getId());
                    intent.putExtra("image_url", current.getImage_url());

                    v.getContext().startActivity(intent);
                }
            });
        }
    }

    public List<Pokemon> pokemon = new ArrayList<>();
    public List<Pokemon> filtered = pokemon;
    private RequestQueue requestQueue;
    PokedexAdapter(Context context) {
        requestQueue = Volley.newRequestQueue(context);
        loadPokemon();
    }

    public void loadPokemon() {
        String url = "https://pokeapi.co/api/v2/pokemon?limit=151";
        final String image_url2 = "https://pokeres.bastionbot.org/images/pokemon/";
        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                try {
                    JSONArray results = response.getJSONArray("results");
                    for (int i = 0; i < results.length(); i++) {
                        JSONObject result = results.getJSONObject(i);
                        String name = result.getString("name");
                        pokemon.add(new Pokemon(
                            name.substring(0, 1).toUpperCase() + name.substring(1),
                            result.getString("url"),image_url2 + Integer.toString(i + 1) + ".png", i + 1));
                    }

                    notifyDataSetChanged();
                } catch (JSONException e) {
                    Log.e("cs50", "Json error", e);
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.e("cs50", "Pokemon list error", error);
            }
        });

        requestQueue.add(request);
    }

    @NonNull
    @Override
    public PokedexViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.pokedex_row, parent, false);

        return new PokedexViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull PokedexViewHolder holder, int position) {
        Pokemon current = filtered.get(position);
        holder.textView.setText(current.getName());
        holder.containerView.setTag(current);
    }

    @Override
    public int getItemCount() {
        return filtered.size();
    }

    @Override
    public Filter getFilter(){
        return new PokemonFilter();
    }
    private class PokemonFilter extends Filter{


        @Override
        protected FilterResults performFiltering(CharSequence constraint){
            List<Pokemon> filteredPokemon = new ArrayList<>();
            if (constraint != null) {
                String text = constraint.toString().toLowerCase().trim();
                for (int i = 0; i < pokemon.size(); i++) {
                    if (pokemon.get(i).getName().toLowerCase().contains(text)) {
                        filteredPokemon.add(pokemon.get(i));
                    }
                }
            }
            else{
                filteredPokemon = pokemon;
            }
            FilterResults results = new FilterResults();
            results.values = filteredPokemon;
            results.count = filteredPokemon.size();
            return results;
        }
        @Override
        protected void publishResults(CharSequence constraint, FilterResults results){
            filtered = (List<Pokemon>) results.values;
            notifyDataSetChanged();
        }
    }
}
