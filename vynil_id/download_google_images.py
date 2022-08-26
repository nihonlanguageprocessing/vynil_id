# https://youtu.be/OQydrlSzxnE
"""
This script downloads images from Google search (or Bing search).
As with any download, please make sure you are not violating any copyright terms.
I use this script to download images that help me practice deep learning based
image classification.
DO NOT use downloaded images to train a commercial product --> this most certainly
violates copyright terms.
Do not pip install google_images_download
this gives an error that some images could not be downloadable.
Google changed some things on their side...
The updated repo can be installed using the following command.
pip install git+https://github.com/Joeclinton1/google-images-download.git
Please remember that this method has a limit of 100 images.
OR
You can use bing.
Does not seem ot have a limit on the number of images to download.
pip install bing-image-downloader
"""

from google_images_download import google_images_download

#instantiate the class
response = google_images_download.googleimagesdownload()
arguments = {"keywords":"Anri (2) - Bi・Ki・Ni, Anri (2) - Coool, Anri (2) - Timely!!, Anri (2) - Wave, Hiroshi Sato - Aqua, Hiroshi Sato - Awakening, Hiroshi Sato - Future File, Hiroshi Sato - Sound Of Science, Mariya Takeuchi - Beginning, Mariya Takeuchi - Love Songs, Mariya Takeuchi - Miss M, Mariya Takeuchi - Request, Mariya Takeuchi - Trad = トラッド, Mariya Takeuchi - University Street, Momoko Kikuchi - Adventure, Momoko Kikuchi - Escape From Dimension, Momoko Kikuchi - Ocean Side, Momoko Kikuchi - Tropic Of Capricorn =トロピック・オブ・カプリコーン 南回帰線, Taeko Ohnuki - Aventure, Taeko Ohnuki - Cliche, Taeko Ohnuki - Grey Skies, Taeko Ohnuki - Mignonne, Taeko Ohnuki - Romantique, Taeko Ohnuki - Sunshower, Tatsuro Yamashita - Big Wave = ビッグウェイブ, Tatsuro Yamashita - Circus Town, Tatsuro Yamashita - For You, Tatsuro Yamashita - Go Ahead!, Tatsuro Yamashita - It's A Poppin' Time, Tatsuro Yamashita - Melodies, Tatsuro Yamashita - Moonglow, Tatsuro Yamashita - On The Street Corner, Tatsuro Yamashita - On The Street Corner 2, Tatsuro Yamashita - Ride On Time, Tatsuro Yamashita - Softly, Tatsuro Yamashita - Spacy, Utada Hikaru - Badモード, Utada Hikaru - Deep River, Utada Hikaru - First Love, Various - Classic Jazz-Funk Mastercuts Volume 7, 東北新幹線 - Thru Traffic",
             "limit":3,"print_urls":False
             }

paths = response.download(arguments)

#print complete paths to the downloaded images
print(paths)
