package com.example.sort_it_json

import okhttp3.MultipartBody
import retrofit2.Call
import retrofit2.http.Field
import retrofit2.http.FormUrlEncoded
import retrofit2.http.GET
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part

interface ApiService {
    @GET("health")
    fun health(): Call<HealthResponse>

    @Multipart
    @POST("predict")
    fun predict(@Part file: MultipartBody.Part): Call<PredictResponse>

    @FormUrlEncoded
    @POST("feedback")
    fun feedback(
        @Field("predicted") predicted: String,
        @Field("correct") correct: String,
    ): Call<FeedbackResponse>
}
