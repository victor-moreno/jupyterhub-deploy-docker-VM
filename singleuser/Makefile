
include ../.env

imageM:
	docker build -t jupyter-minimal \
	    --file Dockerfile-minimal \
		.

imageF:
	docker build -t jupyter-full \
	    --file Dockerfile-full \
		.

imageG:
	docker build -t jupyter-gpu \
	    --file Dockerfile-gpu \
		.

imageC:
	docker build -t jupyter-cuda \
	    --file Dockerfile-cuda \
		.

imageT:
	docker build -t jupyter-torch \
	    --file Dockerfile-torch \
		.

imageR:
	docker build -t jupyter-r \
	    --file Dockerfile-r \
		.
imageRS:
	docker build -t jupyter-rstudio \
	    --file Dockerfile-rs \
		.

imageD:
	docker build -t jupyter-devel \
	    --file Dockerfile-devel \
		.

imageS:
	docker build -t jupyter-snpimpute \
	    --file Dockerfile-snpimpute \
		.

imageZ:
	docker build -t jupyter-deepzoom \
	    --file Dockerfile-deepzoom \
		.

imageV:
	docker build -t jupyter-vnc \
	    --file Dockerfile-vnc \
		.


all14:	imageF imageM imageR imageRS imageS imageZ imageV imageG imageC imageT 
all00:	imageF imageM imageR imageRS imageS imageZ imageV
