package com.example.sort_it_json

data class PredictResponse(
    val recyclable: Boolean,
    val message: String? = null,
    val material: String? = null,
    val subcategory: String? = null,
)

data class HealthResponse(
    val status: String,
)

data class FeedbackResponse(
    val status: String,
)
