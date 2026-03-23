plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace = "com.example.sort_it_json"
    compileSdk {
        version = release(36)
    }


    defaultConfig {
        applicationId = "com.example.sort_it_json"
        minSdk = 24
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"
        buildConfigField("String", "API_BASE_URL", "\"http://10.0.2.2:8000/\"")

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        debug {
            buildConfigField("String", "API_BASE_URL", "\"http://10.0.2.2:8000/\"")
        }
        release {
            isMinifyEnabled = false
            buildConfigField("String", "API_BASE_URL", "\"https://your-api-domain/\"")
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = "11"
    }

    //Renaming apk file
    applicationVariants.all {
        outputs.all {
            // Cast required to access outputFileName property
            val outputImpl = this as com.android.build.gradle.internal.api.BaseVariantOutputImpl

            val appName = "Sort-It" // <-- NAME

            outputImpl.outputFileName = "${appName}.apk"
        }
    }
}

dependencies {
        // Gson for JSON parsing
        implementation("com.google.code.gson:gson:2.13.2")
    implementation("com.squareup.retrofit2:retrofit:2.11.0")
    implementation("com.squareup.retrofit2:converter-gson:2.11.0")
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
    implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
        implementation("androidx.core:core-splashscreen:1.0.0")
        implementation("com.tbuonomo:dotsindicator:5.1.0")
        implementation("androidx.webkit:webkit:1.8.0")
        implementation(libs.androidx.core.ktx)
        implementation(libs.androidx.appcompat)
        implementation(libs.material)
        implementation(libs.androidx.activity)
        implementation(libs.androidx.constraintlayout)
        testImplementation(libs.junit)
        androidTestImplementation(libs.androidx.junit)
        androidTestImplementation(libs.androidx.espresso.core)

        implementation ("androidx.camera:camera-camera2:1.3.0")
        implementation ("androidx.camera:camera-lifecycle:1.3.0")
        implementation ("androidx.camera:camera-view:1.3.0")
    }