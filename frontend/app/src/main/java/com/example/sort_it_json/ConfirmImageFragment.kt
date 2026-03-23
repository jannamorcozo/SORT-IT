package com.example.sort_it_json

import android.net.Uri
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.io.File

class ConfirmImageFragment : Fragment() {

    private lateinit var imageView: ImageView
    private lateinit var statusText: TextView
    private lateinit var analyzeButton: Button
    private var photoPath: String? = null

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_confirm_image, container, false)

        imageView = view.findViewById(R.id.imageView)
        statusText = view.findViewById(R.id.statusText)
        analyzeButton = view.findViewById(R.id.btnAnalyze)

        photoPath = arguments?.getString("photo_path")
        if (photoPath != null) {
            imageView.setImageURI(Uri.fromFile(File(photoPath)))
        } else {
            statusText.text = "No photo found"
            analyzeButton.isEnabled = false
        }

        analyzeButton.setOnClickListener {
            submitForPrediction()
        }

        return view
    }

    private fun submitForPrediction() {
        val currentPhotoPath = photoPath ?: return
        val photoFile = File(currentPhotoPath)
        if (!photoFile.exists()) {
            Toast.makeText(requireContext(), "Image file not found", Toast.LENGTH_SHORT).show()
            return
        }

        analyzeButton.isEnabled = false
        statusText.text = "Analyzing image..."

        val requestBody = photoFile.asRequestBody("image/jpeg".toMediaType())
        val multipartFile = MultipartBody.Part.createFormData("file", photoFile.name, requestBody)

        ApiClient.service.predict(multipartFile).enqueue(object : Callback<PredictResponse> {
            override fun onResponse(call: Call<PredictResponse>, response: Response<PredictResponse>) {
                analyzeButton.isEnabled = true
                if (!response.isSuccessful || response.body() == null) {
                    statusText.text = "Prediction failed"
                    Toast.makeText(requireContext(), "Prediction failed (${response.code()})", Toast.LENGTH_SHORT).show()
                    return
                }

                val data = response.body()!!
                val fragment = RecyclableresultFragment().apply {
                    arguments = Bundle().apply {
                        if (!data.recyclable) {
                            putString("category", "NonRec")
                        } else {
                            putString("category", mapMaterialToUiCategory(data.material))
                            putString("subcategory", mapSubcategoryToUiKey(data.subcategory))
                        }
                    }
                }

                parentFragmentManager.beginTransaction()
                    .replace(R.id.fragment_container, fragment)
                    .addToBackStack(null)
                    .commit()
            }

            override fun onFailure(call: Call<PredictResponse>, t: Throwable) {
                analyzeButton.isEnabled = true
                statusText.text = "Request failed"
                Toast.makeText(requireContext(), "Network error: ${t.message}", Toast.LENGTH_SHORT).show()
            }
        })
    }

    private fun mapMaterialToUiCategory(material: String?): String {
        return when (material?.lowercase()) {
            "plastic" -> "Plastic"
            "glass" -> "Glass"
            "metal" -> "Metal"
            "paper" -> "Paper"
            "residual" -> "Residual"
            else -> "NonRec"
        }
    }

    private fun mapSubcategoryToUiKey(subcategory: String?): String {
        return when (subcategory) {
            "Bottle" -> "glassBottles"
            "Flat" -> "flatGlass"
            "Cullets" -> "cullets"
            "Aluminum_Tin" -> "aluminum_tin"
            "Copper" -> "copper"
            "Steel" -> "steel"
            "Flexible Plastics" -> "CDFP"
            "Leather" -> "leather"
            "Textiles" -> "textiles"
            "Rubber" -> "rubber"
            "Other" -> "others"
            else -> subcategory ?: ""
        }
    }

    /**
     * Deletes the photo file at the given path.
     * Call this after you’re done with the photo to remove it.
     */
    fun deletePhoto(photoPath: String) {
        val file = File(photoPath)
        if (file.exists()) {
            val deleted = file.delete()
            if (deleted) {
                // File deleted successfully
                println("Photo deleted: $photoPath")
            } else {
                // Failed to delete
                println("Failed to delete photo: $photoPath")
            }
        }
    }
}