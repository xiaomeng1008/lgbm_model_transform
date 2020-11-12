LightGBM Model Transform

  LightGBM Model is usually deployed through Java for efficiency in production. We trans Model Model to form like this:
  
    Tree 0
    
    leaf_no  node_type          feature_no   num_threshold        cate_threshold left_child  right_child  is_leaf_node
    
    Tree 1
    
    leaf_no  node_type          feature_no   num_threshold        cate_threshold left_child  right_child  is_leaf_node
    
    ... ...
    
    
  The transformed model can be read for inference and prediction through Java, and the leaf node number can be output.Later, we will improve the Java call part of the code, and finally realize that the final score and leaf node number can be output through Java call.


Prerequisites

LightGBM 2.0.0 or newer.

Python 3.6 or newer.

