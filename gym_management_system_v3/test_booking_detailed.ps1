$headers = @{
    'Authorization' = 'Token 03fa2317a6fea2d7d4fc5df2b6340e30604f9084'
    'Content-Type' = 'application/json'
}

$body = @{
    facility_id = 1
    booking_date = '2025-06-20'
    start_time = '10:00'
    end_time = '12:00'
    person_count = 1
    remark = 'Test booking'
} | ConvertTo-Json

Write-Host "Request Body: $body"

try {
    $response = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/bookings/create/' -Method POST -Headers $headers -Body $body
    Write-Host "Success: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response Body: $responseBody"
        $reader.Close()
    }
}