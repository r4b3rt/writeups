package com.example.re;

import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    public native String checkFromJNI(String str);

    public native String stringFromJNITest();

    static {
        System.loadLibrary("native-test");
    }

    protected void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        setContentView((int) R.layout.activity_main);
        final EditText editText = (EditText) findViewById(R.id.editText);
        ((Button) findViewById(R.id.button)).setOnClickListener(new OnClickListener() {
            public void onClick(View view) {
                view = MainActivity.this.checkFromJNI(editText.getText().toString().trim());
                if (view.equals("1f03d3ddd728d543fd11c7211190d5b7")) {
                    Toast.makeText(MainActivity.this, view, 0).show();
                    Toast.makeText(MainActivity.this, "You win!!!!!!!!", 0).show();
                    return;
                }
                Toast.makeText(MainActivity.this, view, 0).show();
            }
        });
        ((TextView) findViewById(R.id.sample_text)).setText(stringFromJNITest());
    }
}
