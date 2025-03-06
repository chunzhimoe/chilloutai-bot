import os
import fal_client
import asyncio
import logging
from config import DEFAULT_MODEL, DEFAULT_PARAMS, CONTROLNET_MODELS, IP_ADAPTER_CONFIG

logger = logging.getLogger(__name__)

async def upload_image(file_path):
    """
    Upload an image to fal.ai and get the URL
    
    Args:
        file_path (str): Path to the image file
    
    Returns:
        str: URL of the uploaded image
    """
    try:
        logger.info(f"Uploading image: {file_path}")
        
        # Use asyncio to run the synchronous fal_client.upload_file in a separate thread
        loop = asyncio.get_event_loop()
        url = await loop.run_in_executor(
            None,
            lambda: fal_client.upload_file(file_path)
        )
        
        logger.info(f"Image uploaded successfully: {url}")
        return url
    except Exception as e:
        logger.error(f"Error uploading image: {str(e)}")
        raise

async def generate_image(prompt, model=DEFAULT_MODEL, **kwargs):
    """
    Generate an image using fal.ai API
    
    Args:
        prompt (str): The text prompt to generate the image from
        model (str): The model to use for generation
        **kwargs: Additional parameters to pass to the model
    
    Returns:
        dict: The API response containing the image URL
    """
    try:
        # Combine default params with any custom params
        arguments = DEFAULT_PARAMS.copy()
        arguments.update(kwargs)
        arguments["prompt"] = prompt
        
        logger.info(f"Generating image with prompt: {prompt[:100]}...")
        
        # Use asyncio to run the synchronous fal_client.subscribe in a separate thread
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: fal_client.subscribe(
                model,
                arguments=arguments,
                with_logs=True
            )
        )
        
        logger.info("Image generated successfully")
        return result
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        raise

async def generate_with_controlnet(prompt, image_url, controlnet_type="canny", model=DEFAULT_MODEL, **kwargs):
    """
    Generate an image using ControlNet
    
    Args:
        prompt (str): The text prompt to guide image generation
        image_url (str): URL of the control image
        controlnet_type (str): Type of controlnet to use (canny, depth, pose, etc.)
        model (str): The model to use for generation
        **kwargs: Additional parameters to pass to the model
    
    Returns:
        dict: The API response containing the generated image
    """
    try:
        # Get the appropriate controlnet path
        controlnet_path = CONTROLNET_MODELS.get(controlnet_type, CONTROLNET_MODELS["canny"])
        
        # Create ControlNet config
        controlnet = {
            "path": controlnet_path,
            "control_image_url": image_url,
            "conditioning_scale": kwargs.pop("conditioning_scale", 0.8)
        }
        
        # Add other optional ControlNet parameters if provided
        if "start_percentage" in kwargs:
            controlnet["start_percentage"] = kwargs.pop("start_percentage")
        if "end_percentage" in kwargs:
            controlnet["end_percentage"] = kwargs.pop("end_percentage")
        
        # Add controlnet to arguments
        kwargs["controlnet"] = controlnet
        
        # Generate the image
        return await generate_image(prompt, model, **kwargs)
    except Exception as e:
        logger.error(f"Error generating with controlnet: {str(e)}")
        raise

async def generate_with_ip_adapter(prompt, image_url, model=DEFAULT_MODEL, **kwargs):
    """
    Generate an image using IP-Adapter
    
    Args:
        prompt (str): The text prompt to guide image generation
        image_url (str): URL of the reference image
        model (str): The model to use for generation
        **kwargs: Additional parameters to pass to the model
    
    Returns:
        dict: The API response containing the generated image
    """
    try:
        # Create IP-Adapter config
        ip_adapter = IP_ADAPTER_CONFIG.copy()
        ip_adapter["image_url"] = image_url
        
        # Update with custom scale if provided
        if "ip_adapter_scale" in kwargs:
            ip_adapter["scale"] = kwargs.pop("ip_adapter_scale")
        
        # Add IP-Adapter to arguments
        kwargs["ip_adapter"] = ip_adapter
        
        # Generate the image
        return await generate_image(prompt, model, **kwargs)
    except Exception as e:
        logger.error(f"Error generating with IP-Adapter: {str(e)}")
        raise
