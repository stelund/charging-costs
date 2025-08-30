import datetime
from unittest.mock import Mock

import zaptec


def test_list_chargers(monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = {
        "Pages": 1,
        "Data": [
            {
                "OperatingMode": 3,
                "IsOnline": True,
                "Id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "MID": "ZPR123456",
                "DeviceId": "ZPR123456",
                "SerialNo": "Parkering A12",
                "Name": "Charger 1",
                "CreatedOnDate": "2025-06-05T07:30:24.043",
                "CircuitId": "11111111-2222-3333-4444-555555555555",
                "Active": True,
                "CurrentUserRoles": 3,
                "Pin": "0000",
                "DeviceType": 1,
                "InstallationName": "Test Installation",
                "InstallationId": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                "AuthenticationType": 0,
                "IsAuthorizationRequired": False,
            },
            {
                "OperatingMode": 1,
                "IsOnline": True,
                "Id": "f1e2d3c4-b5a6-9870-fedc-ba0987654321",
                "MID": "ZPG654321",
                "DeviceId": "ZPG654321",
                "SerialNo": "Parkering B33",
                "Name": "Charger 2",
                "CreatedOnDate": "2025-06-05T07:30:46.363",
                "CircuitId": "11111111-2222-3333-4444-555555555555",
                "Active": True,
                "CurrentUserRoles": 3,
                "Pin": "0000",
                "DeviceType": 1,
                "InstallationName": "Test Installation",
                "InstallationId": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                "AuthenticationType": 0,
                "IsAuthorizationRequired": False,
            },
            {
                "OperatingMode": 1,
                "IsOnline": True,
                "Id": "12345678-90ab-cdef-1234-567890abcdef",
                "MID": "ZPR789012",
                "DeviceId": "ZPR789012",
                "SerialNo": "Parkering B21",
                "Name": "Charger 3",
                "CreatedOnDate": "2025-06-05T07:31:08.137",
                "CircuitId": "11111111-2222-3333-4444-555555555555",
                "Active": True,
                "CurrentUserRoles": 3,
                "Pin": "0000",
                "DeviceType": 1,
                "InstallationName": "Test Installation",
                "InstallationId": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                "AuthenticationType": 0,
                "IsAuthorizationRequired": False,
            },
        ],
    }
    mock_response.raise_for_status.return_value = None

    def mock_make_request(method, endpoint, **kwargs):
        return mock_response

    monkeypatch.setattr("zaptec.make_authenticated_request", mock_make_request)

    result = zaptec.list_chargers()

    assert len(result) == 3
    assert result[0]["Name"] == "Charger 1"
    assert result[0]["IsOnline"] is True
    assert result[1]["Name"] == "Charger 2"
    assert result[1]["IsOnline"] is True
    assert result[2]["Name"] == "Charger 3"


def test_get_energy_history(monkeypatch):
    mock_response = Mock()
    mock_response.json.return_value = {
        "Pages": 1,
        "Data": [
            {
                "StartDateTime": "2025-06-07T09:20:55.967",
                "EndDateTime": "2025-06-07T16:46:56.877",
                "Energy": 2.527,
                "CommitMetadata": 21,
                "CommitEndDateTime": "2025-06-07T16:46:56.877",
                "ChargerId": "xxx",
                "DeviceName": "xxx",
                "ExternallyEnded": True,
                "EnergyDetails": [
                    {"Timestamp": "2025-06-07T09:20:55.943+00:00", "Energy": 0.0},
                    {"Timestamp": "2025-06-07T09:30:01.007+00:00", "Energy": 0.509},
                    {"Timestamp": "2025-06-07T09:45:00.584+00:00", "Energy": 0.883},
                    {
                        "Timestamp": "2025-06-07T10:00:00.281+00:00",
                        "Energy": 0.6560000000000001,
                    },
                    {
                        "Timestamp": "2025-06-07T10:15:00.752+00:00",
                        "Energy": 0.36599999999999966,
                    },
                    {
                        "Timestamp": "2025-06-07T10:30:00.683+00:00",
                        "Energy": 0.11300000000000043,
                    },
                    {"Timestamp": "2025-06-07T16:46:56.864+00:00", "Energy": 0.0},
                ],
                "ChargerFirmwareVersion": {
                    "Major": 5,
                    "Minor": 0,
                    "Build": 7,
                    "Revision": 2,
                    "MajorRevision": 0,
                    "MinorRevision": 2,
                },
                "SignedSession": 'OCMF|{"FV":"1.0","GI":"Zaptec Pro MID","GS":"ZPR294591","GV":"5.0.7.2","PG":"T1","MF":"v1.3.6","IS":false,"RD":[{"TM":"2025-06-07T09:20:55,943+00:00 R","TX":"B","RV":0.842,"RI":"1-0:1.8.0","RU":"kWh","ST":"G"},{"TM":"2025-06-07T09:30:01,007+00:00 R","TX":"T","RV":1.351,"RI":"1-0:1.8.0","ST":"G"},{"TM":"2025-06-07T09:45:00,584+00:00 R","TX":"T","RV":2.234,"RI":"1-0:1.8.0","ST":"G"},{"TM":"2025-06-07T10:00:00,281+00:00 R","TX":"T","RV":2.89,"RI":"1-0:1.8.0","ST":"G"},{"TM":"2025-06-07T10:15:00,752+00:00 R","TX":"T","RV":3.256,"RI":"1-0:1.8.0","ST":"G"},{"TM":"2025-06-07T10:30:00,683+00:00 R","TX":"T","RV":3.369,"RI":"1-0:1.8.0","ST":"G"},{"TM":"2025-06-07T16:46:56,864+00:00 R","TX":"E","RV":3.369,"RI":"1-0:1.8.0","ST":"G"}],"ZS":"29ebc8fc-04a6-4ff7-bd9e-a6ca3982493b"}|{"SA":"ECDSA-secp384r1-SHA256","SE":"base64","SD":"MGUCMQDoF1zV4648++T9/idWQSa+mybjhEhzsvHWYNL1LaKAWMAMDz8jnkDQ3ff02DIqC3gCMHOuHK0Wnbh6hQT1oFUYhW5EVF927sUfUQoxq6je3w43DY6xYRl8pJLXdQ/nDwQ0ag=="}',
            },
            {
                "Id": "e2e4b400-2569-4323-ad7c-569eab7d6403",
                "DeviceId": "ZPR294591",
                "StartDateTime": "2025-06-05T15:23:18.443",
                "EndDateTime": "2025-06-07T08:19:58.73",
                "Energy": 0.842,
                "CommitMetadata": 21,
                "CommitEndDateTime": "2025-06-07T08:19:58.73",
                "ChargerId": "xxx",
                "DeviceName": "xxx",
                "ExternallyEnded": True,
                "EnergyDetails": [
                    {"Timestamp": "2025-06-05T15:23:18.337+00:00", "Energy": 0.0},
                    {"Timestamp": "2025-06-05T15:30:00.26+00:00", "Energy": 0.365},
                    {"Timestamp": "2025-06-05T15:45:00.206+00:00", "Energy": 0.364},
                    {
                        "Timestamp": "2025-06-05T16:00:01.004+00:00",
                        "Energy": 0.11299999999999999,
                    },
                    {"Timestamp": "2025-06-07T08:19:58.714+00:00", "Energy": 0.0},
                ],
            },
        ],
    }
    mock_response.raise_for_status.return_value = None

    def mock_make_request(method, endpoint, **kwargs):
        return mock_response

    monkeypatch.setattr("zaptec.make_authenticated_request", mock_make_request)

    from_date = datetime.datetime.now()
    to_date = datetime.datetime.now()
    result, charges_count = zaptec.get_energy_history("xxx", from_date, to_date)

    assert len(result) == 12
    assert charges_count == 2
