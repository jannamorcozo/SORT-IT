import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf

# Folder containing your .keras models
keras_models_folder = "."  # Current directory where the .keras files are
tflite_output_folder = "tflite_models/"

# Make sure output folder exists
os.makedirs(tflite_output_folder, exist_ok=True)

# Loop through all .keras files in the folder
for file_name in os.listdir(keras_models_folder):
    if file_name.endswith(".keras"):
        keras_path = os.path.join(keras_models_folder, file_name)
        try:
            print(f"Loading {keras_path}...")
            model = tf.keras.models.load_model(keras_path)

            # Convert to TFLite
            converter = tf.lite.TFLiteConverter.from_keras_model(model)

            # Optional: quantization to reduce size
            # converter.optimizations = [tf.lite.Optimize.DEFAULT]
            # converter.target_spec.supported_types = [tf.float16]

            tflite_model = converter.convert()

            # Save with same base name but .tflite extension
            tflite_path = os.path.join(
                tflite_output_folder, file_name.replace(".keras", ".tflite")
            )
            with open(tflite_path, "wb") as f:
                f.write(tflite_model)

            print(f"✓ Converted {file_name} → {tflite_path}")
        except Exception as e:
            print(f"✗ Error converting {file_name}: {str(e)}")
            import traceback
            traceback.print_exc()
