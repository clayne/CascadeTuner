import torch
# from diffusers import AutoencoderKL
# from diffusers.utils.import_utils import is_xformers_available
from PIL import Image
import numpy as np
from tokeniser_util import tokenize_respecting_boundaries

# batch = torch.load("E:\\sd1_latents\\latent_cache_your_sd1_finetune_0.pt")

# Load the VAE model
# vae = AutoencoderKL.from_pretrained("X:\sd1-5", subfolder="vae")
# vae.to("cuda:0")
# vae.requires_grad_(False)
# vae.enable_slicing()
# if is_xformers_available():
# 	try:
# 		vae.enable_xformers_memory_efficient_attention()
# 	except Exception as e:
# 		print("no xformers")

# # Function to decode latents
# def decode_latents(latents):
# 	latents = 1 / 0.18215 * (latents.sample() * 0.18215)
# 	with torch.no_grad():
# 		image = vae.decode(latents).sample

# 	image = (image / 1).clamp(0, 1)
# 	image = image.detach().cpu().permute(0, 2, 3, 1).numpy()
# 	images = (image * 255).round().astype("uint8")
# 	pil_images = [Image.fromarray(image) for image in images]
# 	return pil_images

# decoded_images = decode_latents(batch["vae_encoded"])
# decoded_images[0].save("decoded_image.png")

from transformers import CLIPTokenizer
tokenizer = CLIPTokenizer.from_pretrained("X:\sd1-5", subfolder="tokenizer")

# This is some VLM slop to test how it handles tokenisation of boundaries
test_batch = [
	"This is a digital anime-style drawing depicting a sexual scene. The main focus is on a woman with long, wavy blue hair and striking green eyes. She has a fair complexion and is topless, her large breasts prominently displayed. Her expression is one of pleasure, with a slightly open mouth and flushed cheeks.",
	"She is lying on a red surface, possibly a bed, and is being held by a pair of large, dark-skinned hands, which are grabbing her breasts from underneath. Her breasts are positioned directly in front of the viewer, with a visible censor bar covering her nipples. The background is minimalistic, focusing entirely on the woman and the hands.",
	"The artist's signature, '@puch-11744,' is visible in the top left corner of the image. The image has a glossy texture, indicative of modern digital art. The style is typical of adult anime, characterized by exaggerated features, bright colors, and a focus on eroticism. The overall tone is explicit and intended for an adult audience."
]

# Compare respected boundaries vs regular CLIP encoding
test_tokens, test_mask = tokenize_respecting_boundaries(tokenizer, test_batch)

for partial in test_tokens:
	decoded_texts = tokenizer.batch_decode(partial, skip_special_tokens=True)
	pos = 0
	for text in decoded_texts:
		print(pos, text)
		pos+=1

orig_tokens = tokenizer(
	test_batch,
	padding=False,
	add_special_tokens=False,
	verbose=False
).input_ids

print("")
print("---")
print("")

orig_texts = tokenizer.batch_decode(orig_tokens, skip_special_tokens=True)
pos = 0
for text in orig_texts:
	print(pos, text)
	pos+=1