cd results
git init && git add -A && git commit -m "deploy" 
git push -f git@github.com:nobeam/lattice-summaries-data.git master:results
cd - 
