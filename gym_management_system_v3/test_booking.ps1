try {
    $headers = @{
        'Content-Type' = 'application/json'
        'Authorization' = 'Token 03fa2317a6fea2d7d4fc5df2b6340e30604f9084'
    }
    
    $body = @{
        facility_id = 1
        booking_date = '2024-01-01'
        start_time = '10:00'
        end_time = '11:00'
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/bookings/create/' -Method POST -Headers $headers -Body $body
    Write-Host "Status: $($response.StatusCode)"
    Write-Host "Content: $($response.Content)"
} catch {
    Write-Host "Error: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response Body: $responseBody"
        $reader.Close()
    }
}