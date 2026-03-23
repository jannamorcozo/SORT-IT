package com.example.sort_it_json

import android.os.Bundle                       // Used to pass data between fragments
import android.view.LayoutInflater             // Used to inflate XML layout
import android.view.View                       // Base view class
import android.view.ViewGroup                  // Layout container
import android.widget.Button                   // Button UI element
import android.widget.Toast                    // For showing short messages
import androidx.camera.core.CameraSelector
import androidx.camera.core.ImageCapture
import androidx.camera.core.ImageCaptureException
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.app.ActivityCompat
import androidx.fragment.app.Fragment          // Base Fragment class
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import java.io.File                            // Used to create file for saving image
import androidx.core.content.ContextCompat     // Used to check permissions

// Define the fragment class
class CameraFragment : Fragment() {

    private lateinit var previewView: PreviewView
    private lateinit var captureButton: Button
    private lateinit var cameraExecutor: ExecutorService
    private var imageCapture: ImageCapture? = null

    // Request code for permission request (used to identify permission result)
    private val CAMERA_PERMISSION_CODE = 100

    // Called when the fragment UI is being created
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {

        // Inflate the layout XML into a View object
        val view = inflater.inflate(R.layout.fragment_camera, container, false)

        previewView = view.findViewById(R.id.previewView)
        captureButton = view.findViewById(R.id.capture_button)
        cameraExecutor = Executors.newSingleThreadExecutor()

        return view // Return the created view
    }

    // Called after the view is created (safe to interact with UI here)
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Check if camera permission is already granted
        if (ContextCompat.checkSelfPermission(requireContext(), android.Manifest.permission.CAMERA)
            == android.content.pm.PackageManager.PERMISSION_GRANTED
        ) {
            startCamera()
            enableCameraButton() // If granted -> enable capture button
        } else {
            // If not granted → request permission from user
            ActivityCompat.requestPermissions(
                requireActivity(),
                arrayOf(android.Manifest.permission.CAMERA),
                CAMERA_PERMISSION_CODE
            )
        }
    }

    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(requireContext())
        cameraProviderFuture.addListener({
            val cameraProvider = cameraProviderFuture.get()

            val preview = Preview.Builder().build().also {
                it.surfaceProvider = previewView.surfaceProvider
            }

            imageCapture = ImageCapture.Builder()
                .setCaptureMode(ImageCapture.CAPTURE_MODE_MINIMIZE_LATENCY)
                .build()

            val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA

            try {
                cameraProvider.unbindAll()
                cameraProvider.bindToLifecycle(
                    viewLifecycleOwner,
                    cameraSelector,
                    preview,
                    imageCapture
                )
            } catch (exc: Exception) {
                Toast.makeText(requireContext(), "Failed to start camera", Toast.LENGTH_SHORT).show()
            }
        }, ContextCompat.getMainExecutor(requireContext()))
    }

    // Function to enable button and set click behavior
    private fun enableCameraButton() {

        // Enable the button so user can click it
        captureButton.isEnabled = true

        // Set click listener
        captureButton.setOnClickListener {
            takePhoto()
        }
    }

    private fun takePhoto() {
        val capture = imageCapture ?: return

        val photoFile = File(
            requireContext().getExternalFilesDir(null),
            "photo_${SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(Date())}.jpg"
        )

        val outputOptions = ImageCapture.OutputFileOptions.Builder(photoFile).build()

        capture.takePicture(
            outputOptions,
            cameraExecutor,
            object : ImageCapture.OnImageSavedCallback {
                override fun onError(exception: ImageCaptureException) {
                    requireActivity().runOnUiThread {
                        Toast.makeText(requireContext(), "Failed to capture photo", Toast.LENGTH_SHORT).show()
                    }
                }

                override fun onImageSaved(outputFileResults: ImageCapture.OutputFileResults) {
                    requireActivity().runOnUiThread {
                        val bundle = Bundle().apply {
                            putString("photo_path", photoFile.absolutePath)
                        }

                        val fragment = ConfirmImageFragment().apply {
                            arguments = bundle
                        }

                        parentFragmentManager.beginTransaction()
                            .replace(R.id.fragment_container, fragment)
                            .addToBackStack(null)
                            .commit()
                    }
                }
            }
        )
    }

    // Called after user responds to permission request
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)

        // Check if this result is for camera permission
        if (requestCode == CAMERA_PERMISSION_CODE) {

            // Check if permission was granted
            if ((grantResults.isNotEmpty() &&
                        grantResults[0] == android.content.pm.PackageManager.PERMISSION_GRANTED)
            ) {
                startCamera()
                enableCameraButton() // Permission granted → enable camera
            } else {
                // Permission denied → show message
                Toast.makeText(requireContext(), "Camera permission is required to take photos", Toast.LENGTH_SHORT).show()
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        cameraExecutor.shutdown()
    }
}