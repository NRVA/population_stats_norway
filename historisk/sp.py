

historikk = {
      "query": [
        {
          "code": "Region",
          "selection": {
            "filter": "agg:KommSummer",
            "values": [

            ]
          }
        },
        {
          "code": "Kjonn",
          "selection": {
            "filter": "item",
            "values": [
            ]
          }
        },
        {
          "code": "Alder",
          "selection": {
            "filter": "agg:TredeltGrupperingB2",
            "values": [
              "F0-19",
              "F20-64",
              "F65+"
            ]
          }
        }
      ],
      "response": {
        "format": "json-stat2"
      }
    }