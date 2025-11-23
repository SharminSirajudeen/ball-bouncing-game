package com.example.bouncingball

import android.os.Bundle
import android.view.WindowManager
import androidx.appcompat.app.AppCompatActivity
import com.example.bouncingball.databinding.ActivityMainBinding
import com.example.bouncingball.dialog.ColorPickerDialog
import com.google.android.material.snackbar.Snackbar

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Set up view binding
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        // Keep screen on while playing
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        
        // Set up FAB click listener
        setupFabListener()
        
        // Show welcome message
        showWelcomeMessage()
    }

    private fun setupFabListener() {
        binding.fabSettings.setOnClickListener {
            showColorPickerDialog()
        }
    }

    private fun showColorPickerDialog() {
        val currentColor = binding.ballGameView.getBallColor()
        
        ColorPickerDialog(currentColor) { selectedColor ->
            binding.ballGameView.setBallColor(selectedColor)
            Snackbar.make(
                binding.root,
                "Ball color changed!",
                Snackbar.LENGTH_SHORT
            ).show()
        }.show(supportFragmentManager, ColorPickerDialog.TAG)
    }

    private fun showWelcomeMessage() {
        Snackbar.make(
            binding.root,
            "Tap anywhere to make the ball bounce!",
            Snackbar.LENGTH_LONG
        ).show()
    }
}