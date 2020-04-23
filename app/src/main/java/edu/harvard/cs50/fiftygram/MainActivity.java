package edu.harvard.cs50.fiftygram;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.os.Bundle;
import android.os.ParcelFileDescriptor;
import android.provider.MediaStore;
import android.view.View;
import android.widget.ImageView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.Transformation;
import com.bumptech.glide.request.RequestOptions;
import com.bumptech.glide.request.target.CustomTarget;
import com.bumptech.glide.request.transition.Transition;

import java.io.FileDescriptor;
import java.io.IOException;

import jp.wasabeef.glide.transformations.BlurTransformation;
import jp.wasabeef.glide.transformations.GrayscaleTransformation;
import jp.wasabeef.glide.transformations.gpu.PixelationFilterTransformation;
import jp.wasabeef.glide.transformations.gpu.SepiaFilterTransformation;
import jp.wasabeef.glide.transformations.gpu.SketchFilterTransformation;
import jp.wasabeef.glide.transformations.gpu.ToonFilterTransformation;

public class MainActivity extends AppCompatActivity implements ActivityCompat.OnRequestPermissionsResultCallback{
    private ImageView imageView;
    private Bitmap original;
    private Bitmap filtered;
    private String outputfile;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        outputfile= "original";
        imageView = findViewById(R.id.image_view);
        original = BitmapFactory.decodeResource(this.getResources(), R.drawable.template);
        filtered = original;
        Glide
                .with(this)
                .load(original)
                .into(imageView);
    }
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }
    public void apply(Transformation<Bitmap> filter) {
        if (original != null) {
            Glide
                    .with(this)
                    .asBitmap()
                    .load(original)
                    .placeholder(R.drawable.template)
                    .apply(RequestOptions.bitmapTransform(filter))
                    .into(new CustomTarget<Bitmap>() {
                @Override
                public void onResourceReady(@NonNull Bitmap resource, @Nullable Transition<? super Bitmap> transition) {
                    filtered = resource;
                    imageView.setImageBitmap(resource);
                }
                @Override
                public void onLoadCleared(@Nullable Drawable placeholder) {
                }
            });
        }
    }

    public void returnOriginal(View view) {
        Glide
                .with(this)
                .load(original)
                .placeholder(R.drawable.template)
                .into(imageView); outputfile="Original"; filtered = original;
    }
    public void applySepia(View view) { apply(new SepiaFilterTransformation()); outputfile="Sepia";}

    public void applyToon(View view) {
        apply(new ToonFilterTransformation()); outputfile="Toon";
    }

    public void applySketch(View view) {
        apply(new SketchFilterTransformation());outputfile="Sketch";
    }

    public void applyPixel(View view) { apply(new PixelationFilterTransformation());outputfile="Pixel"; }

    public void applyGrayscale(View view) { apply(new GrayscaleTransformation());outputfile="Grayscale"; }

    public void applyBlur(View view) { apply(new BlurTransformation());outputfile="Blur"; }
    public void saveButton(View view) {
        requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
        String value = MediaStore.Images.Media.insertImage(getContentResolver(), filtered, "Output_" + outputfile + ".png", "Produced by fiftygram");
        AlertDialog.Builder alert = new AlertDialog.Builder(this);
        if (value != null) {

            alert.setTitle("Saved To the Galery");
            alert.setMessage("As a file :" + " Output_" + outputfile + ".png .");
            alert.show();
        }
        else{
            alert.setTitle("Permission Denied");
            alert.setMessage("You have to allow program to write on your disk.");
            alert.show();
        }
    }

    public void choosePhoto(View view) {
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.setType("image/*");
        startActivityForResult(intent, 1);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == Activity.RESULT_OK && data != null) {
            try {
                Uri uri = data.getData();
                ParcelFileDescriptor parcelFileDescriptor =
                        getContentResolver().openFileDescriptor(uri, "r");
                FileDescriptor fileDescriptor = parcelFileDescriptor.getFileDescriptor();
                original = BitmapFactory.decodeFileDescriptor(fileDescriptor);
                parcelFileDescriptor.close();
                imageView.setImageBitmap(original);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
