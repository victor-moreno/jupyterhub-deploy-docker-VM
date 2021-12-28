rsync -avn --exclude={data,bck,.git,.env,'z cuda.odap-ico.org',sync.sh} ./ bck/genrisk/
rsync -avn --exclude={data,bck,.git,.env,'z remote.genrisk.org'} bck/genrisk/ ./
