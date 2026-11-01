# Assemblers do not consistently report .incbin files in their dependency output.
# Incremental generation can change images while preserving identical assembly.
file(GLOB RC_GENERATED_IMAGES CONFIGURE_DEPENDS
    "${SSR_GENERATED_DIR}/rc_image_*.bin")
set_property(SOURCE "${SSR_GENERATED_DIR}/rc_images.S"
    APPEND PROPERTY OBJECT_DEPENDS "${RC_GENERATED_IMAGES}")
