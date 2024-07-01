import telebot
import cv2
from polybot.img_proc import Img
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
# Check if TELEGRAM_TOKEN is not none
if TELEGRAM_TOKEN is None:
    print("Error  : TELEGRAM_TOKEN is not set in the .env file.")
    exit(1)

# initialize telegram-bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Dictionary to store images temporarily
user_images = {}


# handler for the /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Hello!\n\n Send me an image then choose a filter , options:\n"
                                      "- Blur: Apply a blur to the image to reduce noise and detail.\n"
                                      "- Rotate: turning the image upside down.\n"
                                      "- Salt and Pepper: Adds random bright and dark pixels to an image.\n"
                                      "- Segment: Divides an image into parts based on color.\n"
                                      "- Grayscale: Converts the image to grayscale.\n"
                                      "- Sharpen: Enhances the edges and details in the image.\n"
                                      "- Emboss: Creates a raised effect by highlighting the edges.\n"
                                      "- Invert Colors: Inverts the colors of the image.\n"
                                      "- Oil Painting: Applies an oil painting-like effect to the image.\n"
                                      "- Cartoonize: Creates a cartoon-like version of the image.\n")


# handler for receiving photos
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    try:
        print("Received a photo message")
        # get the photo file id
        file_id = message.photo[-1].file_id
        # get the file object using the file id
        file_info = bot.get_file(file_id)
        # download the file
        downloaded_file = bot.download_file(file_info.file_path)

        # save the file temporarily with a unique name based on the file id
        image_path = f"images/{file_id}.jpg"
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # check if this is the first img or the second img for concat
        if message.chat.id in user_images:
            print("User already has an image in memory")
            if 'concat_pending' in user_images[message.chat.id]:
                print("This is the second image for concatenation")
                # this is the second image for concat
                second_image_path = image_path
                first_image_path = user_images[message.chat.id]['concat_pending']
                del user_images[message.chat.id]['concat_pending']  # remove the pending to free it to next pending

                # load the images
                first_image_data = cv2.imread(first_image_path)
                second_image_data = cv2.imread(second_image_path)

                # concat the imges
                img_processor = Img(first_image_path)
                concatenated_image = img_processor.concat(second_image_data)
                if concatenated_image is not None:
                    print("Concatenation successful")
                    # save and send the concat img
                    processed_image_path = img_processor.save_image(concatenated_image, suffix='_concatenated')
                    with open(processed_image_path, 'rb') as photo_file:
                        bot.send_photo(message.chat.id, photo_file)
                else:
                    print("Error concatenating images.")
                    bot.reply_to(message, "Error concatenating images.")

                # clear user history
                del user_images[message.chat.id]
            else:
                # this is the first img
                print("This is the first image for concatenation")
                user_images[message.chat.id]['concat_pending'] = image_path
                bot.reply_to(message,
                             "First image saved successfully! Now please send the second image to concatenate with.")
        else:
            # this is the first img
            print("This is the first image received")
            user_images[message.chat.id] = {'concat_pending': image_path}
            bot.reply_to(message,
                         "First image saved successfully! To apply the concatenation filter, please send another image or choose a filter from the list at the top of the page to apply a filter.")
    except Exception as e:
        print(f"Error handling image: {e}")
        bot.reply_to(message, f"Error handling image: {e}")


# handler for filter selection
@bot.message_handler(
    func=lambda message: message.text.lower() in ['blur', 'rotate', 'salt and pepper', 'segment', 'grayscale',
                                                  'sharpen', 'emboss', 'invert colors', 'oil painting', 'cartoonize'])
def handle_filter(message):
    try:
        # Check if the user has previously sent an image
        if message.chat.id in user_images:
            # Get the image path
            if 'concat_pending' in user_images[message.chat.id]:
                image_path = user_images[message.chat.id]['concat_pending']
            else:
                image_path = user_images[message.chat.id]['first_image']

            # apply the selected filter
            img_processor = Img(image_path)
            filter_name = message.text.lower()

            if filter_name == 'blur':
                processed_image = img_processor.blur()
            elif filter_name == 'rotate':
                processed_image = img_processor.rotate()
            elif filter_name == 'salt and pepper':
                processed_image = img_processor.salt_n_pepper()
            elif filter_name == 'segment':
                processed_image = img_processor.segment()
            elif filter_name == 'grayscale':
                processed_image = img_processor.grayscale()
            elif filter_name == 'sharpen':
                processed_image = img_processor.sharpen()
            elif filter_name == 'emboss':
                processed_image = img_processor.emboss()
            elif filter_name == 'invert colors':
                processed_image = img_processor.invert_colors()
            elif filter_name == 'oil painting':
                processed_image = img_processor.oil_painting()
            elif filter_name == 'cartoonize':
                processed_image = img_processor.cartoonize()
            else:
                processed_image = None

            # check if the filter was applied successfully
            if processed_image is not None:
                # save and send the processed image
                processed_image_path = img_processor.save_image(processed_image,
                                                                suffix=f'_{filter_name.replace(" ", "_")}')
                with open(processed_image_path, 'rb') as photo_file:
                    bot.send_photo(message.chat.id, photo_file)
            else:
                bot.reply_to(message, f"Error applying {filter_name} filter: Result is None.")

            # remove the image path from the dict
            del user_images[message.chat.id]
        else:
            bot.reply_to(message, "Please send an image first.")
    except Exception as e:
        bot.reply_to(message, f"Error processing image: {e}")


bot.polling()
