package com.example.bouncingball.dialog

import android.app.Dialog
import android.os.Bundle
import android.view.LayoutInflater
import androidx.fragment.app.DialogFragment
import com.example.bouncingball.databinding.DialogColorPickerBinding
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.skydoves.colorpickerview.listeners.ColorListener

class ColorPickerDialog(
    private val currentColor: Int,
    private val onColorSelected: (Int) -> Unit
) : DialogFragment() {

    private var _binding: DialogColorPickerBinding? = null
    private val binding get() = _binding!!
    private var selectedColor: Int = currentColor

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        _binding = DialogColorPickerBinding.inflate(LayoutInflater.from(requireContext()))

        setupColorPicker()
        setupButtons()

        return MaterialAlertDialogBuilder(requireContext())
            .setView(binding.root)
            .create()
    }

    private fun setupColorPicker() {
        binding.colorPickerView.apply {
            setInitialColor(currentColor)
            setColorListener(ColorListener { color, _ ->
                selectedColor = color
            })
        }
    }

    private fun setupButtons() {
        binding.btnApply.setOnClickListener {
            onColorSelected(selectedColor)
            dismiss()
        }

        binding.btnCancel.setOnClickListener {
            dismiss()
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    companion object {
        const val TAG = "ColorPickerDialog"
    }
}