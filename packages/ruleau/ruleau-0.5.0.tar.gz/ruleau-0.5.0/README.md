# Ruleau

A Python Rules Engine library

## Using the library

A username and password is required. This can be passed directly to the ApiAdapter (i.e. via the CLI) or these can
be set in the environment variables.

```text
RULEAU_USERNAME=myusername
RULEAU_PASSWORD=mypassword
```

```python
from ruleau import execute, rule, ApiAdapter

# create a rule
@rule(rule_id="rul_1", name="Is adult")
def over_18(_, payload):
    return "age" in payload and payload["age"] >= 18

# create a payload (the answers to the rule's questions)
payload = {"age": 17}

# execute the rule against the payload
result = execute(over_18, payload)

# integrate with the backend web API with password and username in env
api_adapter = ApiAdapter(
    base_url="http://localhost:8000/"
)
# or pass directly to ApiAdapter:
api_adapter = ApiAdapter(
    base_url="http://localhost:8000/", username=myusername, password=mypassword
)

# send the results
result = execute(over_18, payload, api_adapter=api_adapter, case_id="ca_1280")
# result.result will be False due to applicant being 17

# if the rule for this case is overriden in the backend
# then running again will return True

```

### Organisational Data

Optionally a Process can be assigned as set of "tags" called Organisational Data which can be used
to filter or categorise rules and results.

Each Process must have these specified up front by setting the Organisational Scheme like so:

```python
api_adapter = ApiAdapter(
    base_url="http://localhost:8000",
)

org_scheme: List[OrganisationalScheme] = [
    OrganisationalScheme(
        id="location",  # ID Used to refer to the tag when organisational data is posted
        display_name="Location",  # Label used on the UI when being displayed
        display_default=True,  # If true, will appear on the UI by default, otherwise is hidden
        type="string",  # Either a `string`, `integer`, `float` or `date` type
    ),
    OrganisationalScheme(
        id="internal_id",  # ID Used to refer to the tag when organisational data is posted
        display_name="ID",  # Label used on the UI when being displayed
        display_default=True,  # If true, will appear on the UI by default, otherwise is hidden
        type="integer",  # Either a `string`, `integer`, `float` or `date` type
    )
]

api_adapter.publish_organisational_scheme(over_18, org_scheme)
```

Once set data can be provided when a ruleset is executed by updating the API Adapter using its
`with_organisational_data` method like so:

```python
api_adapter = ApiAdapter(
    base_url="http://localhost:8000/"
).with_organisational_data([
    {"key": "location", "value": "Bristol"},
    {"key": "internal_id", "value": 5}
])

result = execute(over_18, payload, api_adapter=api_adapter, case_id="ca_1280")
```

Optionally we can also set the order by which Organisational Data appears on the UI by posting
to the UI Layout Metadata endpoint as in this example:

```python
ui_layout_metadata: UiLayoutMetadata = {
    # Defines the order the tags will appear on the cases page
    "case_org_data_order": [{"id": "internal_id"}, {"id": "location"}],
    # Defines the order the tags will appear on the overrides page
    "override_org_data_order": [{"id": "department"}],
}

api_adapter.publish_ui_layout_metadata(
    payload_has_patient_rule, ui_layout_metadata
)
```

### Testing Rules

Rules should be tested using [doctest](https://docs.python.org/3/library/doctest.html).

Example of these tests can be found in the [Kitchen Sink example](https://gitlab.com/unai-ltd/unai-decision/ruleau-core/-/tree/develop/examples/kitchen_sink/rules.py).

### Generating Documentation

Documentation for the rules can be generated using the `ruleau-docs` command.

The usage is as follows:
```
ruleau-docs [--output-dir=<argument>] filename
```

For example for a file of rules called `rules.py` run:
```
ruleau-docs rules.py
```

## Building & Testing the Library

### Pre-requisites

* [Python 3.9+](https://www.python.org/downloads/)

Package requirements installed by running:

```shell
pip install -r requirements-dev.txt
```

### Running the Tests

To run all unit tests in the project use the following command:

```shell
pytest
```
