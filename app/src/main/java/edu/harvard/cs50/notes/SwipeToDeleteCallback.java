package edu.harvard.cs50.notes;

import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.PorterDuff;
import android.graphics.drawable.ColorDrawable;
import android.view.View;

import androidx.recyclerview.widget.ItemTouchHelper;
import androidx.recyclerview.widget.RecyclerView;


public class SwipeToDeleteCallback extends ItemTouchHelper.SimpleCallback {
    private NotesAdapter mAdapter;
    private final ColorDrawable background;

    SwipeToDeleteCallback(NotesAdapter adapter) {
        super(0, ItemTouchHelper.RIGHT);
        background = new ColorDrawable(Color.RED);
        mAdapter = adapter;
    }

    @Override
    public void onSwiped(RecyclerView.ViewHolder viewHolder, int direction) {
        if (direction == ItemTouchHelper.RIGHT) {
            int position = mAdapter.notes.get(viewHolder.getAdapterPosition()).id;
            mAdapter.deleteItem(position);

            mAdapter.reload();
        }
    }
    @Override
    public boolean onMove(RecyclerView viewHolder, RecyclerView.ViewHolder a, RecyclerView.ViewHolder b) {
        mAdapter.reload();
        return true;
    }
    @Override
    public void onChildDraw(Canvas c, RecyclerView recyclerView, RecyclerView.ViewHolder viewHolder, float dX, float dY, int actionState, boolean isCurrentlyActive) {
        super.onChildDraw(c, recyclerView, viewHolder, dX,
                dY, actionState, isCurrentlyActive);
        View itemView = viewHolder.itemView;
        int backgroundCornerOffset = 20;
        if (dX > 0) { // Swiping to the right
            background.setBounds(itemView.getLeft(), itemView.getTop(),
                    itemView.getLeft() + ((int) dX) + backgroundCornerOffset,
                    itemView.getBottom());

        } else if (dX < 0) { // Swiping to the left
            background.setBounds(itemView.getRight() + ((int) dX) - backgroundCornerOffset,
                    itemView.getTop(), itemView.getRight(), itemView.getBottom());
        } else { // view is unSwiped
            background.setBounds(0, 0, 0, 0);
        }
        background.draw(c);
    }
}