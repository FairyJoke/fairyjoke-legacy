def extractor(xml, definition, target):
    '''
    Assigns members of an object from an XML node according to a definition
    mapping dict

    Keys of the mapping dict defines members to assign.
    Values of the mapping dict can be either: None, String, Dict or Callables
    - If they are None, the XML node with the name of the key is assigned
    - If they are a String, the XML node which matches the string is assigned
    - If they are a Dict, they can contain the following key-values:
        - 'key': assigns the value just like with a simple String, evaluates to
            the mapping key if None
        - 'fun': assigns the result of the function stored at value with the XML
            node string matched by 'key' passed as parameter
    - If they are a Callable, the whole XML node is passed to it and the result
        of that is assigned

    See app/sdvx/models.py "from_xml" methods for examples

    :param xml: An XML node from ElementTree
    :param definition: A dict that represents a definition mapping
    :param target: Where to assign the result
    '''

    # print('XML extractor initiated on', xml)
    for key in definition:
        rule = definition.get(key) or key
        if isinstance(rule, str):
            tag = xml.find(rule)
            if tag is None:
                print('Could not find {}, ignoring...'.format(rule))
                continue
            value = tag.text
        elif callable(rule):
            value = rule(xml)
        elif isinstance(rule, dict):
            name = rule.get('key', key)
            tag = xml.find(name)
            if tag is None:
                print('Could not find {}, ignoring...'.format(name))
                continue
            value = rule['fun'](tag.text)
        else:
            print('Unrecognized definition mapping {}, ignoring...'.format(rule))
            continue
        setattr(target, key, value)
        # print('Assigned', key, 'to', value)
    # print('Finished updating', target)

