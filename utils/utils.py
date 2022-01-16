

def get_dependencies(df, target_name, target_col='target', source_col='source'):
    depend_list = df[df[target_col] == target_name][source_col].tolist()
    return '<br>'.join(depend_list) if len(depend_list) > 0 else 'No dependencies found'

def get_properties(df, table_name, table_name_col='table_name'):
    properties = df[df[table_name_col] == table_name].to_dict('records')[0]
    return properties

def get_options():
    var_options = (
        '''
        var options = {
            "layout": {
                "hierarchical": {
                    "enabled": true,
                    "edgeMinimization": true,
                    "direction": "LR",
                    "sortMethod": "directed"
                }
            },
            "edges": {
                "physics": true,
                "smooth": {
                    "enabled": true,
                    "type": "cubicBezier",
                    "roundness": 0.70
                },
                "arrows": {
                    "to": {
                        "enabled": true,
                        "scaleFactor": 0.4,
                        "type": "arrow"
                    },
                    "middle": {
                        "enabled": false,
                        "scaleFactor": 0.4
                    },
                    "from": {
                        "enabled": false,
                        "scaleFactor": 0.4,
                        "type": "arrow"
                    }
                }
            }
        }
        '''
    )
    return var_options