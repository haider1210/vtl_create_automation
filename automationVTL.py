import json
from airspeed import Template

# Define the JSON data
json_data = '''
{
  "provider": {
    "changebootable-1": "openstackcliProvider.openstackCLI"
  },
  "command": {
    "cmd": "volume set"
  },
  "args": {
    "required": {
      "value-1":"diskid",
      "if_then_else": {
        "bootable==true": ["bootable", "non-bootable"],
        "Ab==8" :["smile" ,"happy"]
      }
    },
    "optional": {
      "Oa_value-1":"Oa_diskid",
      "if_then_else": {
        "Oa_bootable==true": ["Oa_bootable", "Oa_non-bootable"],
        "Oa_Ab==8" :["Oasmile" ,"Oahappy"]
      }
    }
  },
  "flags": {
    "required": {
      "fr_value-1":"fr_diskid",
      "if_then_else": {
        "fr_bootable==true": ["fr_bootable", "fr_non-bootable"],
        "fr_Ab==8" :["fr_smile" ,"fr_happy"]
      }
    },
    "optional": {
      "Of_value-1":"Of_diskid",
      "if_then_else": {
        "Of_bootable==true": ["Of_bootable", "Of_non-bootable"],
        "Of_Ab==8" :["Ofsmile" ,"Ofhappy"]
      }
    }
  },
  "properties": {
    "required": {
       "format":false,
       "insecure":true
     }
  }
}
'''

# Convert JSON to dictionary
data_dict = json.loads(json_data)

# Extract relevant parts from the JSON data
path = "$path"
prvdr = data_dict["provider"]
cmnd = data_dict["command"]["cmd"]

args_req = data_dict["args"]["required"]
args_opt = data_dict["args"]["optional"]
a_req_if_then_else = args_req.get("if_then_else", {})
a_opt_if_then_else = args_opt.get("if_then_else", {})

flgs_req = data_dict["flags"]["required"]
flgs_opt = data_dict["flags"]["optional"]
f_req_if_then_else = flgs_req.get("if_then_else", {})
f_opt_if_then_else = flgs_opt.get("if_then_else", {})

provider_name_key = list(data_dict["provider"].keys())[0]
hss = "#"

pro_req = data_dict["properties"]["required"]

# Generate the output using Airspeed Template
template = Template('''
Command Template: {
  "group": {
    #foreach ($key in $prvdr.keySet())"$key" : "$prvdr.get($key)"#if($foreach.hasNext),#end
    #end
  },
  "commands": {
    "group.${provider_name_key}.cmd": "$cmnd",
    #foreach($key in $args_req.keySet())#if($key == "if_then_else") #foreach($cond in $a_req_if_then_else.keySet())
    "group.${provider_name_key}.args.${foreach.count}": "${hss}if($path.$cond)--${a_req_if_then_else[$cond][0]}${hss}else--${a_req_if_then_else[$cond][1]}${hss}end",#end
    #else"group.${provider_name_key}.args.${foreach.count}": "$path.${args_req[$key]}", #end#end
    #foreach($key in $args_opt.keySet()) #if($key == "if_then_else")
    #foreach($cond in $a_opt_if_then_else.keySet())
    "group.${provider_name_key}.args.${foreach.count}": "${hss}if($path.$cond)--${a_opt_if_then_else[$cond][0]}${hss}else--${a_opt_if_then_else[$cond][1]}${hss}end",#end#else
    "group.${provider_name_key}.args.${foreach.count}": "$path.${args_opt[$key]}",#end#end
    
    #############################
    
    #foreach($key in $flgs_req.keySet())#if($key == "if_then_else") #foreach($cond in $f_req_if_then_else.keySet())
    "group.${provider_name_key}.flags.${foreach.count}": "${hss}if($path.$cond)--${f_req_if_then_else[$cond][0]}${hss}else--${f_req_if_then_else[$cond][1]}${hss}end",#end
    #else"group.${provider_name_key}.flags.${foreach.count}": "$path.${flgs_req[$key]}",#end#end
    #foreach($key in $flgs_opt.keySet()) #if($key == "if_then_else")
    #foreach($cond in $f_opt_if_then_else.keySet())
    "group.${provider_name_key}.flags.${foreach.count}": "${hss}if($path.$cond)--${f_opt_if_then_else[$cond][0]}${hss}else--${f_opt_if_then_else[$cond][1]}${hss}end", #end#else
    "group.${provider_name_key}.flags.${foreach.count}": "$path.${flgs_opt[$key]}", #end#end
    #foreach($key in $pro_req.keySet())
    "group.${provider_name_key}.properties.${key}": ${pro_req[$key]}#if($foreach.hasNext),#end#end
  },
  "response": {
    "out": {
      "quantity": 1,
      "details": [
        {
          "id": "${transaction.order_lines[0].node.configurations.config_attributes.diskid}",
          "type": "${transaction.order_lines[0].node.provider_resource_type}"
        }
      ]
    }
  }
}
''')

# Merge the template with the local variables
output = template.merge(locals())
print(output)
