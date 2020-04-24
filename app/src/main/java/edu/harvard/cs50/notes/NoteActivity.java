package edu.harvard.cs50.notes;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

import com.google.android.material.floatingactionbutton.FloatingActionButton;

public class NoteActivity extends AppCompatActivity {
    private EditText editText;
    protected int id;
    protected FloatingActionButton fab;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_note);

        Intent intent = getIntent();
        editText = findViewById(R.id.note_edit_text);
        editText.setText(intent.getStringExtra("content"));
        id = intent.getIntExtra("id",1);
        fab = findViewById(R.id.delete_note_button);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();
                MainActivity.database.noteDao().delete(id);
            }
        });

    }

    @Override
    protected void onPause() {
        super.onPause();

        Intent intent = getIntent();
        MainActivity.database.noteDao().save(editText.getText().toString(), id);


    }
    public void delete_note_button(View view){

    }
}
