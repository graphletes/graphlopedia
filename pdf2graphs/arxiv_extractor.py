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
		images = pdf2graphs.parse_tex(path.join(output_folder,document))
	
		# unable to read file
		if not images:
			arxiv_reader.skipped.append(arxiv_reader.article)
			continue

		for image in images:
			if type(image) is dict:
				info = open(path.join(write_folder,'info.txt'), 'w+')
				info.write(json.dumps(image))
				info.close()
		
			elif image[0] in documents:
				copyfile(path.join(output_folder,image[0]), path.join(write_folder,image[0]))
				image_name, _ = path.splitext(image[0])
				if len(image[1]) > 0:
					tag_file = open(path.join(write_folder, "%s.tag" % image_name),'w+')
					for tag in image[1]:
						tag_file.write("%s\n" % tag)

					tag_file.close()

	elif '.pdf' in exts:
		document = documents[exts.index('.pdf')]
		pdf2graphs.extract(path.join(output_folder,document),write=write_folder)

	written = listdir(write_folder)
	if not (len(written) == 1 and 'info.txt' in written):
		arxiv_reader.write()

arxiv_reader.close()

