package com.example.sort_it_json

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class feedbackFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_feedback, container, false)

        val predictedInput = view.findViewById<EditText>(R.id.etPredicted)
        val correctInput = view.findViewById<EditText>(R.id.etCorrect)
        val submitButton = view.findViewById<Button>(R.id.btnSubmitFeedback)

        submitButton.setOnClickListener {
            val predicted = predictedInput.text.toString().trim()
            val correct = correctInput.text.toString().trim()

            if (predicted.isEmpty() || correct.isEmpty()) {
                Toast.makeText(requireContext(), "Please complete both fields", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            submitButton.isEnabled = false
            ApiClient.service.feedback(predicted, correct).enqueue(object : Callback<FeedbackResponse> {
                override fun onResponse(call: Call<FeedbackResponse>, response: Response<FeedbackResponse>) {
                    submitButton.isEnabled = true
                    if (response.isSuccessful) {
                        Toast.makeText(requireContext(), "Feedback submitted", Toast.LENGTH_SHORT).show()
                        parentFragmentManager.beginTransaction()
                            .replace(R.id.fragment_container, HomeFragment())
                            .addToBackStack(null)
                            .commit()
                    } else {
                        Toast.makeText(requireContext(), "Failed to submit (${response.code()})", Toast.LENGTH_SHORT).show()
                    }
                }

                override fun onFailure(call: Call<FeedbackResponse>, t: Throwable) {
                    submitButton.isEnabled = true
                    Toast.makeText(requireContext(), "Network error: ${t.message}", Toast.LENGTH_SHORT).show()
                }
            })
        }

        return view
    }
}