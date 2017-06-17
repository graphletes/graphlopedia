import json
import arxiv
import pdf2graphs
import argparse

from shutil import copyfile
from os import mkdir, listdir, path

parser = argparse.ArgumentParser(description="extracts and runs pdf2graphs on arXiv tar")
parser.add_argument('arxiv', type=str, help='name of arxiv to process')
parser.add_argument('output', type=str, help='name of output tar')
args = parser.parse_args()

output_folder = 'art'
write_folder = 'wrt'

# for tar_arxiv in os.listdir(directory):
arxiv_reader = arxiv.helper(args.arxiv, write_name=args.output, write=write_folder, output=output_folder, messages=True)

# extract next article
while arxiv_reader.next_article():
	documents = listdir(output_folder)
	if not path.isdir(write_folder):
		mkdir(write_folder)
	
	exts = [path.splitext(document)[1] for document in documents]

	if '.tex' in exts:
		document = documents[exts.index('.tex')]
		
		# parse tex file, retrieve source image filenames
		images, info = pdf2graphs.parse_tex(path.join(output_folder,document))
		if info:
			info_file = open(path.join(write_folder,'info.json'), 'w+')
			info_file.write(json.dumps(info))
			info_file.close()
				

		# unable to read file
		if not images:
			arxiv_reader.skipped.append(arxiv_reader.article)
			continue

		for image in images:
			try:
				if type(image) is str:
					copyfile(path.join(output_folder,image), path.join(write_folder,image))

				elif type(image) is tuple:
					copyfile(path.join(output_folder,image[0]), path.join(write_folder,image[0]))
					if image[1]:
						image_name, _ = path.splitext(image[0])
						tag_file = open(path.join(write_folder, "%s.txt" % image_name),'w+')
						tag_file.write(image[1])
						tag_file.close()

			except FileNotFoundError:
				# file not included in tar for some reason
				if type(image) is str:
					print("%s not found" % image)
				elif type(image) is tuple:
					print("%s not found" % image[0])

	elif '.pdf' in exts:
		document = documents[exts.index('.pdf')]
		pdf2graphs.extract(path.join(output_folder,document),write=write_folder)

	written = listdir(write_folder)
	if not (len(written) == 1 and 'info.txt' in written):
		arxiv_reader.write()

arxiv_reader.close()

