rsync -avn --delete --exclude={data,bck,.git,.env,'*.org',sync.sh} ./ bck/genrisk/
rsync -avn --delete --exclude={data,bck,.git,.env,'*.org',sync.sh} bck/genrisk/ ./
