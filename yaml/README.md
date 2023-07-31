# Existing YAML Recipes

By default, BLAZE's drag-and-drop builder will store newly created YAML files in the `yaml/` folder. 

The following YAML files are currently provided as default recipes to experiment with: 

* `01_search_custom.yaml` - Uses a hybrid of Elasticsearch and BERT for Q/A on user-uploaded `.txt` files 
* `02_search_benchmark.yaml` - Benchmarks this hybrid of Elasticsearch and BERT on SQUAD 2.0 dataset 
* `03_search_comparison.yaml`- Benchmarks and compares two versions of ElasticBERT models on SQUAD 2.0
* `04_summary_custom.yaml` - Uses BART for summarization on user-uploaded `.txt` files `

&nbsp;&nbsp;

We have additional YAML files as well in the `debug_yaml/` folder, but these are currently undergoing slight stabilization. 

Additionally, we will be adding YAML recipes for our two sample WebEx integrations soon! 
