from openai import OpenAI
import re
import json

client = OpenAI(api_key="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")

nsx_api = 'Distributed Firewall Rule Creation API'
request_body_schema = '''
    {
      "description": "A rule indicates the action to be performed for various types of traffic flowing between workload groups.",
      "id": "Rule",
      "module_id": "Policy",
      "properties": {
          "action": {
              "description": "The action to be applied to all the services The JUMP_TO_APPLICATION action is only supported for rules created in the Environment category. Once a match is hit then the rule processing will jump to the rules present in the Application category, skipping all further rules in the Environment category. If no rules match in the Application category then the default application rule will be hit. This is applicable only for DFW.",
              "enum": [
                  "ALLOW",
                  "DROP",
                  "REJECT",
                  "JUMP_TO_APPLICATION"
              ],
              "title": "Action",
              "type": "string"
          },
          "description": {
              "can_sort": true,
              "maxLength": 1024,
              "title": "Description of this resource",
              "type": "string"
          },
          "destination_groups": {
              "description": "We need paths as duplicate names may exist for groups under different domains. Along with paths we support IP Address of type IPv4 and IPv6. IP Address can be in one of the format(CIDR, IP Address, Range of IP Address). In order to specify all groups, use the constant \"ANY\". This is case insensitive. If \"ANY\" is used, it should be the ONLY element in the group array. Error will be thrown if ANY is used in conjunction with other values.",
              "items": {
                  "type": "string"
              },
              "maxItems": 128,
              "required": false,
              "title": "Destination group paths",
              "type": "array"
          },
          "destinations_excluded": {
              "default": false,
              "description": "If set to true, the rule gets applied on all the groups that are NOT part of the destination groups. If false, the rule applies to the destination groups",
              "readonly": false,
              "required": false,
              "title": "Negation of destination groups",
              "type": "boolean"
          },
          "direction": {
              "default": "IN_OUT",
              "description": "Define direction of traffic.",
              "enum": [
                  "IN",
                  "OUT",
                  "IN_OUT"
              ],
              "required": false,
              "title": "Direction",
              "type": "string"
          },
          "disabled": {
              "default": false,
              "description": "Flag to deactivate the rule. Default is activated.",
              "readonly": false,
              "required": false,
              "title": "Flag to deactivate the rule",
              "type": "boolean"
          },
          "display_name": {
              "can_sort": true,
              "computed": true,
              "description": "Defaults to ID if not set",
              "maxLength": 255,
              "title": "Identifier to use when displaying entity in logs or GUI",
              "type": "string"
          },
          "id": {
              "can_sort": true,
              "title": "Unique identifier of this resource",
              "type": "string"
          },
          "ip_protocol": {
              "description": "Type of IP packet that should be matched while enforcing the rule. The value is set to IPV4_IPV6 for Layer3 rule if not specified. For Layer2/Ether rule the value must be null.",
              "enum": [
                  "IPV4",
                  "IPV6",
                  "IPV4_IPV6"
              ],
              "readonly": false,
              "required": false,
              "title": "IPv4 vs IPv6 packet type",
              "type": "string"
          },
          "is_default": {
              "description": "A flag to indicate whether rule is a default rule.",
              "readonly": true,
              "required": false,
              "title": "Default rule flag",
              "type": "boolean"
          },
          "logged": {
              "default": false,
              "description": "Flag to enable packet logging. Default is deactivated.",
              "readonly": false,
              "title": "Enable logging flag",
              "type": "boolean"
          },
          "marked_for_delete": {
              "default": false,
              "description": "Intent objects are not directly deleted from the system when a delete is invoked on them. They are marked for deletion and only when all the realized entities for that intent object gets deleted, the intent object is deleted. Objects that are marked for deletion are not returned in GET call. One can use the search API to get these objects.",
              "readonly": true,
              "required": false,
              "title": "Indicates whether the intent object is marked for deletion",
              "type": "boolean"
          },
          "notes": {
              "description": "Text for additional notes on changes.",
              "maxLength": 2048,
              "readonly": false,
              "required": false,
              "title": "Text for additional notes on changes",
              "type": "string"
          },
          "origin_site_id": {
              "description": "This is a UUID generated by the system for knowing which site owns an object. This is used in NSX+.",
              "readonly": true,
              "required": false,
              "title": "A unique identifier assigned by the system for knowing which site owns an object",
              "type": "string"
          },
          "overridden": {
              "default": false,
              "description": "Global intent objects cannot be modified by the user. However, certain global intent objects can be overridden locally by use of this property. In such cases, the overridden local values take precedence over the globally defined values for the properties.",
              "readonly": true,
              "required": false,
              "title": "Indicates whether this object is the overridden intent object",
              "type": "boolean"
          },
          "owner_id": {
              "description": "This is a UUID generated by the system for knowing who owns this object. This is used in NSX+.",
              "readonly": true,
              "required": false,
              "title": "A unique identifier assigned by the system for the ownership of an object",
              "type": "string"
          },
          "parent_path": {
              "description": "Path of its parent",
              "readonly": true,
              "required": false,
              "title": "Path of its parent",
              "type": "string"
          },
          "path": {
              "description": "Absolute path of this object",
              "readonly": true,
              "required": false,
              "title": "Absolute path of this object",
              "type": "string"
          },
          "profiles": {
              "description": "Holds the list of layer 7 service profile paths. These profiles accept attributes and sub-attributes of various network services (e.g. L4 AppId, encryption algorithm, domain name, etc) as key value pairs. Instead of Layer 7 service profiles you can use a L7 access profile. One of either Layer 7 service profiles or L7 Access Profile can be used in firewall rule. In case of L7 access profile only one is allowed.",
              "items": {
                  "type": "string"
              },
              "maxItems": 128,
              "required": false,
              "title": "Layer 7 service profiles or TLS action profile",
              "type": "array"
          },
          "realization_id": {
              "description": "This is a UUID generated by the system for realizing the entity object. In most cases this should be same as 'unique_id' of the entity. However, in some cases this can be different because of entities have migrated their unique identifier to NSX Policy intent objects later in the timeline and did not use unique_id for realization. Realization id is helpful for users to debug data path to correlate the configuration with corresponding intent.",
              "readonly": true,
              "required": false,
              "title": "A unique identifier assigned by the system for realizing intent",
              "type": "string"
          },
          "relative_path": {
              "description": "Path relative from its parent",
              "readonly": true,
              "required": false,
              "title": "Relative path of this object",
              "type": "string"
          },
          "remote_path": {
              "description": "This is the path of the object on the local managers when queried on the NSX+ service, and path of the object on NSX+ service when queried from the local managers.",
              "readonly": true,
              "required": false,
              "title": "Path of the object on the remote end.",
              "type": "string"
          },
          "resource_type": {
              "description": "The type of this resource.",
              "readonly": false,
              "type": "string"
          },
          "rule_id": {
              "description": "This is a unique 4 byte positive number that is assigned by the system.  This rule id is passed all the way down to the data path. The first 1GB (1000 to 2^30) will be shared by GM and LM with zebra style striped number space. For E.g 1000 to (1Million -1) by LM, (1M - 2M-1) by GM and so on.",
              "readonly": true,
              "required": false,
              "title": "Unique rule ID",
              "type": "integer"
          },
          "scope": {
              "description": "The list of policy paths where the rule is applied LR/Edge/T0/T1/LRP etc. Note that a given rule can be applied on multiple LRs/LRPs.",
              "items": {
                  "type": "string"
              },
              "maxItems": 128,
              "required": false,
              "type": "array"
          },
          "sequence_number": {
              "description": "This field is used to resolve conflicts between multiple Rules under Security or Gateway Policy for a Domain If no sequence number is specified in the payload, a value of 0 is assigned by default. If there are multiple rules with the same sequence number then their order is not deterministic. If a specific order of rules is desired, then one has to specify unique sequence numbers or use the POST request on the rule entity with a query parameter action=revise to let the framework assign a sequence number",
              "minimum": 0,
              "required": false,
              "title": "Sequence number of the this Rule",
              "type": "int"
          },
          "services": {
              "description": "In order to specify all services, use the constant \"ANY\". This is case insensitive. If \"ANY\" is used, it should be the ONLY element in the services array. Error will be thrown if ANY is used in conjunction with other values.",
              "items": {
                  "type": "string"
              },
              "maxItems": 128,
              "required": false,
              "title": "Names of services",
              "type": "array",
          },
          "source_groups": {
              "description": "We need paths as duplicate names may exist for groups under different domains. Along with paths we support IP Address of type IPv4 and IPv6. IP Address can be in one of the format(CIDR, IP Address, Range of IP Address). In order to specify all groups, use the constant \"ANY\". This is case insensitive. If \"ANY\" is used, it should be the ONLY element in the group array. Error will be thrown if ANY is used in conjunction with other values.",
              "items": {
                  "type": "string"
              },
              "maxItems": 128,
              "required": false,
              "title": "Source group paths",
              "type": "array"
          },
          "sources_excluded": {
              "default": false,
              "description": "If set to true, the rule gets applied on all the groups that are NOT part of the source groups. If false, the rule applies to the source groups",
              "readonly": false,
              "required": false,
              "title": "Negation of source groups",
              "type": "boolean"
          },
          "tag": {
              "description": "User level field which will be printed in CLI and packet logs. Even though there is no limitation on length of a tag, internally tag will get truncated after 32 characters.",
              "required": false,
              "title": "Tag applied on the rule",
              "type": "string"
          },
          "unique_id": {
              "description": "This is a UUID generated by the GM/LM to uniquely identify entities in a federated environment. For entities that are stretched across multiple sites, the same ID will be used on all the stretched sites.",
              "readonly": true,
              "required": false,
              "title": "A unique identifier assigned by the system",
              "type": "string"
          }
      },
      "title": "A rule specifies the security policy rule between the workload groups",
      "type": "object"
    }
'''

nsx_api_properties = ['action', 'description', 'destination_groups', 'destinations_excluded', 'direction', 'disabled', 'display_name', 'id', 'ip_protocol', 'is_default', 'logged', 'marked_for_delete', 'notes', 'origin_site_id', 'overridden', 'owner_id', 'parent_path', 'path', 'profiles', 'realization_id', 'relative_path', 'remote_path', 'resource_type', 'rule_id', 'scope', 'sequence_number', 'services', 'source_groups', 'sources_excluded', 'tag', 'unique_id']

def initialize_conversation():
    '''
    Returns a list [{"role": "system", "content": system_message}]
    '''

    delimiter = "####"
    example_user_req = { 'resource_type': 'Rule', 'description': ' comm entry', 'id': 'ce-1', 'display_name': 'ce-1', 'path': '/infra/domains/vmc/security-policies/application-section-1/rules/ce-1', 'relative_path': 'ce-1', 'source_groups': [ '/infra/domains/vmc/groups/dbgroup' ], 'logged': 'false', 'destination_groups': [ '/infra/domains/vmc/groups/appgroup' ], 'scope': [ 'ANY' ], 'action': 'ALLOW', 'services': [ '/infra/services/HTTP', '/infra/services/CIM-HTTP' ] }

    system_message = f"""

    You are an intelligent VMware NSX Config Generator AI assistant and your goal is to generate NSX configuration scripts in python based on user requirements.
    You need to ask relevant questions and populate the {nsx_api} request payload by analysing the user's responses.
    You final objective is to fill the values for the different properties for API's request payload in the python dictionary and be confident of the values.
    {delimiter}These properties of the {nsx_api} request payload are defined below.
    {request_body_schema}
    {delimiter}

    {delimiter}Here are some instructions around the values for the different properties. If you do not follow this, you'll be heavily penalised.
    - The values for all properties in request payload should strictly adhere to the types provided in API documentation.
    - All properties which are required based on {nsx_api} request payload should be collected from user. If the user is not willing to provide details for any such required property, please mention that this is required field for {nsx_api}.
    - All properties which does not have require attribute in schema can be considered as required field.
    - If user tries to set property which has readonly value as true in schema, please mention that the field cannnot be set.
    - If user doesn't specify value of any property, take the default value of the property form schema.
    - Do not randonmly assign values to any of the properties in request payload. The property values need to be inferred from the user's response.
    {delimiter}

    To fill the dictionary, you need to have the following chain of thoughts:
    {delimiter} Thought 1: Ask a question to understand the user's values for {nsx_api} request payload. \n
    You are trying to fill the values of all the properties {nsx_api_properties} in the python dictionary by understanding the user requirements.
    Identify the properties for which you can fill the values confidently using the understanding. \n
    Remember the instructions around the values for the different properties.
    Answer "Yes" or "No" to indicate if you understand the requirements and have updated the values for the relevant properties of {nsx_api} request payload. \n
    If yes, proceed to the next step. Otherwise, rephrase the question to capture these requirements. \n{delimiter}

    {delimiter}Thought 2: Now, you are trying to fill the values for the rest of the properties which you couldn't in the previous step.
    Remember the instructions around the values for the different properties. Ask questions you might have for all the properties of {nsx_api} request payload to strengthen your understanding of the property fields in request payload.
    Answer "Yes" or "No" to indicate if you understood all the values for the keys and are confident about the same.
    If yes, move to the next Thought. If no, ask question on the properties whose values you are unsure of. \n
    It is a good practice to ask question with a sound logic as opposed to directly citing the property you want to understand value for.{delimiter}

    {delimiter}Thought 3: Check if you have correctly updated the values for the different properties in the python dictionary.
    If you are not confident about any of the values, ask clarifying questions. {delimiter}

    Follow the above chain of thoughts and only output the final updated python dictionary. \n


    {delimiter} Here is a sample conversation between the user and assistant:
    User: "Hi, I want to create a distributed firewall rule named 'ce-1' and description 'comm entry'"
    Assistant: "Sure. Do you want to enable logging flag for above rule?"
    User: "Yes please do."
    Assistant: "Do you want to apply this rule to all services or any specific services?"
    User: "Please apply for service with path '/infra/services/HTTP' and '/infra/services/CIM-HTTP'"
    Assistant: "Thank you for the information. What are the paths for source groups and destination groups"
    User: "Include  '/infra/domains/vmc/groups/dbgroup' in source group and '/infra/domains/vmc/groups/appgroup' in destination groups"
    Assistant:"Sure. What action you want to apply on above rule."
    User: "What actions I can apply?"
    Assistant:"You can apply actions like allow, reject and drop"
    User: "Please apply action allow."
    Assistant: "{example_user_req}"
    {delimiter}

    Start with a short welcome message and encourage the user to share their requirements.
    """
    conversation = [{"role": "system", "content": system_message}]
    return conversation

def get_chat_model_completions(messages):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
        max_tokens = 3000
    )
    return response.choices[0].message.content

def moderation_check(user_input):
    response = client.moderations.create(input=user_input)
    moderation_output = response.results[0]
    if moderation_output.flagged == True:
        return "Flagged"
    else:
        return "Not Flagged"
    
def required_properties_populated_confirmation_layer(response_assistant):
    prompt = f"""
    You are a senior evaluator who has an eye for detail.
    You are provided an input. You need to evaluate if the input has the following keys: 'resource_type','display_name', 'id'
    Output a string 'Yes' if the input contains the dictionary with the values correctly filled for all keys.
    Otherwise out the string 'No'.

    Here is the input: {response_assistant}
    Only output a one-word string - Yes/No.
    """


    confirmation = client.chat.completions.create(
                                    model="gpt-4",
                                    messages = [{ 'role': 'user', 'content': prompt }],
                                    temperature=0)


    return confirmation.choices[0].message.content


def dictionary_present(response: str):
    delimiter = "####"
    user_req = '''{
    "resource_type": "Rule",
    "description": "dummy rule",
    "id": "Rule1",
    "display_name": "Rule1",
    "source_groups": ["ANY"],
    "logged": True,
    "destination_groups": ["ANY"],
    "scope": ["ANY"],
    "action": "ALLOW",
    "services": ["ANY"],
    "direction": "IN",
    "sources_excluded": True,
    "destinations_excluded": True,
    "disabled": False
}'''
    prompt = f"""You are a python expert. You are provided an input.
            You have to check if there is a python dictionary present in the string.
            It will have the following format {user_req}.
            Your task is to just extract and return only the python dictionary from the input.
            The output should match the format as {user_req}.
            The output should contain the exact keys and values as present in the input. It shoudlnot contain anything else.

            Here are some sample input output pairs for better understanding:
            {delimiter}
            input: - GPU intensity: low - Display quality: high - Portability: low - Multitasking: high - Processing speed: medium - Budget: 50,000 INR
            output: {{'GPU intensity': 'low', 'Display quality': 'high', 'Portability': 'low', 'Multitasking': 'high', 'Processing speed': 'medium', 'Budget': '50000'}}

            input: {{'GPU intensity':     'low', 'Display quality':     'high', 'Portability':    'low', 'Multitasking': 'high', 'Processing speed': 'medium', 'Budget': '90,000'}}
            output: {{'GPU intensity': 'low', 'Display quality': 'high', 'Portability': 'low', 'Multitasking': 'high', 'Processing speed': 'medium', 'Budget': '90000'}}

            input: Here is your user profile 'GPU intensity': 'high','Display quality': 'high','Portability': 'medium','Multitasking': 'low','Processing speed': 'high','Budget': '200000 INR'
            output: {{'GPU intensity': 'high','Display quality': 'high','Portability': 'medium','Multitasking': 'high','Processing speed': 'low','Budget': '200000'}}
            {delimiter}

            Here is the input {response}

            """
    response = client.chat.completions.create(
        model="gpt-4",
        messages = [{ 'role': 'system', 'content': prompt }],
        max_tokens = 2000
    )
    return response.choices[0].message.content


def extract_dictionary_from_string(string):
    regex_pattern = r"\{[^{}]+\}"

    dictionary_matches = re.findall(regex_pattern, string)

    # Extract the first dictionary match and convert it to lowercase
    if dictionary_matches:
        dictionary_string = dictionary_matches[0]
        dictionary_string = dictionary_string.lower()

        # Convert the dictionary string to a dictionary object using ast.literal_eval()
        dictionary = json.loads(dictionary_string)
    return dictionary

def generate_python_script(response: str):
    prompt = f"""You are a python expert. You are provided an PUT API URL and request body.
            You have to write a python script to execute that API.
            PUT API URL is 'https://<policy-mgr>/policy/api/v1/infra/domains/vmc/security-policies/application-section-1/rules/ce-1'
            Request Body is {response}.
            Your task is to just generate python script to execute given API with given request body.
            The output should contain only python script.
            """
    response = client.chat.completions.create(
        model="gpt-4",
        messages = [{ 'role': 'system', 'content': prompt }],
        max_tokens = 2000
    )
    return response.choices[0].message.content