import json
from airspeed import Template

# Define the JSON data
json_data = '''
{
  "az_vm_create": {
    "provider":{
     "provider_name":"microsoft-azure"
     },
    "command":{
      "cmd" : "az vm create"
     },
    "required": {
      "name": "test",
      "resource-group": "RG",
      "good": "gp",
      "nsg": "nosag",
      "v-cpus-per-core": "VPlus",
      "vnet-name": "VnetNm"
    },
    "optional": {
      "accelerated-networking": ["false", "true"],
      "accept-term": null,
      "admin-password": null,
      "admin-username": null,
      "vmss": null,
      "vnet-address-prefix": null,
      "workspace": null,
      "zone": null
    }
  }
}
'''

# Convert JSON to dictionary
data_dict = json.loads(json_data)

# Get the key of the first item in the dictionary
a = next(iter(data_dict))
b=data_dict[a]["provider"]["provider_name"]
# Access the nested "optional" and "required" dictionaries
optional_dict = data_dict[a]["optional"]
mandatory_dict = data_dict[a]["required"]
cmd=data_dict[a]["command"]

# Generate the output using Airspeed Template
template = Template("""
Command Template: {
  "group": {
        "$a": "$b"
  },
  "commands": {
            #foreach ($key in $cmd.keys())
            "gropu.${a}.${key}" : "${cmd[$key]}", #end
            #foreach ($key in $mandatory_dict.keys())
            "gropu.${a}.${key}" : "${mandatory_dict[$key]}", #end
             #foreach ($key in $optional_dict.keys())
            "group.${a}.${key}" : #if (${optional_dict[$key]}) "${optional_dict[$key]}" #else "" #end, #end

  },
  "response": {
		"out": {
			"quantity": 1,
			"details": [
			{
			  "id": "",
			  "type": ""
			}
        ]
      }
    }
}""")
output = template.merge(locals())
print(output)
