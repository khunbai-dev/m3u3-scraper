from settings import settings
import os, glob, m3u8, grequests, requests  # requests must be behind grequests
from alive_progress import alive_bar


def clear_temp_folder():
  '''
  Description: Remove all files in `/temp` folder except `.gitkeep`
  '''
  dir = settings.BASE_DIR / 'temp'
  for f in os.listdir(dir):
    if f != '.gitkeep':
      os.remove(os.path.join(dir, f))


def save_files(requests):
  '''
  Desc: Get list of requests object and save as .mp4 file in `temp/` folder
  '''
  with alive_bar(len(requests), dual_line=True, title='  [*] Extracting mp4                       ') as bar:
    for r in requests:
      #(v) Extract file name from url for indexing files such as
      #     https://jui02.xyz/videos/5296c3c88cf/5296c3c88cf-1200-0-00009.html
      #     shall become 00009
      file_name = r.url.split('-')[-1].split('.')[0]
      # Save to temp folder
      dir = settings.BASE_DIR / f'temp/{file_name}.mp4'
      open(dir, 'wb').write(r.content)
      bar()


def chunks(lst, n):
  """
    Yield successive n-sized chunks from list.
    Or in other meaning is spliting a list of arbitrary length into equal sized chunks.
  """
  for i in range(0, len(lst), n):
    yield lst[i:i + n]


def concatenate(output_file_name):
  '''
  Desc: Required ffmpeg installed on machine.
  '''

  stringa = "ffmpeg -i \"concat:"
  temp_dir = settings.BASE_DIR / 'temp/*.mp4'
  elenco_video = glob.glob(f'{temp_dir}')
  elenco_file_temp = []
  with alive_bar(len(elenco_video), dual_line=True, title='  [*] Generate ts files                    ') as bar:
    for f in elenco_video:
      temp_dir = f"{settings.BASE_DIR / 'temp'}"
      file = temp_dir + "/temp" + str(elenco_video.index(f) + 1) + ".ts"
      os.system("ffmpeg -i " + f + " -nostats -loglevel 0 -c copy -bsf:v h264_mp4toannexb -f mpegts " + file)
      elenco_file_temp.append(file)
      bar()
  # print(elenco_file_temp)
  for f in elenco_file_temp:
    stringa += f
    if elenco_file_temp.index(f) != len(elenco_file_temp)-1:
      stringa += "|"
    else:
      output_dir = f"{settings.BASE_DIR / 'output'}"
      stringa += "\" -nostats -loglevel 0 -c copy  -bsf:a aac_adtstoasc " + output_dir +'/' + output_file_name +'.mp4' 
  # print(stringa)
  os.system(stringa)


def download(m3u8_url):
  '''
  desc: Extract m3u8 with `m3u8` package to get url list from .m3u8 file and 
        async download with `grequest` package and save each file in temp folder
  '''
  playlist = m3u8.load(m3u8_url)
  set_of_unsent_request = []  # This set to be sent all at the same time by grequests

  index = 0

  for i in playlist.segments:
    split_text = i.uri.split('url=')
    url = split_text[-1]
    set_of_unsent_request.append(grequests.get(url))

    # Print out example of url for checking the result.
    if index == 0:
      print(f'  Example of downloading url "{url}"')

  '''
  Desc: There is no need to divided unsent request object into equal-sized chunks
        actually. But to have alive progress be able to track the progress of total finished
        requests, as inside grequest.map is hidden looping and can not see progress
        , we instead divided list into chunks of unsent requests and
        track finishing of each chunk to see the progress.
  '''
  request_list = []
  #(v) divided list into chunk of 100 items, benefit for alive progress bar
  request_set_chunk = list(chunks(set_of_unsent_request, 100))
  with alive_bar(len(request_set_chunk), dual_line=True, title='  [*] Collecting grequests 100-sized chunks') as bar:
    for request_set in request_set_chunk:
      grequests_list = grequests.map(request_set)
      for r in grequests_list:
        request_list.append(r)
      bar()

  save_files(request_list)


def main():
  print('')
  print('Please enter m3u8 url (ex. https://master.barlow-master.com/api/player/bitrate/5296c3c3b/5296c3c3b-1200-0.m3u8)')
  m3u8_url = input('-> ')
  print('Please enter output file name (ex. output_video)')
  output_file_name = input('-> ')

  clear_temp_folder()
  download(m3u8_url)
  concatenate(output_file_name)
  clear_temp_folder()


if __name__ == "__main__":
	main()