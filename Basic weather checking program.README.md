#include <iostream>
#include <string>
#include <curl/curl.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

size_t WriteCallback(void* contents, size_t size, size_t nmemb, std::string* output) {
    size_t totalSize = size * nmemb;
    output->append((char*)contents, totalSize);
    return totalSize;
}


std::string fetchWeatherData(const std::string& city, const std::string& apiKey) {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;

    std::string url = "https://api.openweathermap.org/data/2.5/weather?q=" + city +
                      "&appid=" + apiKey + "&units=metric";

    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L); // Disable SSL verification for testing
        res = curl_easy_perform(curl);
        if (res != CURLE_OK) {
            std::cerr << "cURL Error: " << curl_easy_strerror(res) << std::endl;
        }
        curl_easy_cleanup(curl);
    }
    return readBuffer;
}


void displayWeather(const std::string& jsonData) {
    try {
        auto data = json::parse(jsonData);

        if (data.contains("main") && data.contains("weather")) {
            std::string cityName = data["name"];
            double temp = data["main"]["temp"];
            double feelsLike = data["main"]["feels_like"];
            int humidity = data["main"]["humidity"];
            std::string weatherDesc = data["weather"][0]["description"];

            std::cout << "\n================ WEATHER DASHBOARD ================\n";
            std::cout << "City: " << cityName << "\n";
            std::cout << "Temperature: " << temp << " °C\n";
            std::cout << "Feels Like: " << feelsLike << " °C\n";
            std::cout << "Humidity: " << humidity << " %\n";
            std::cout << "Condition: " << weatherDesc << "\n";
            std::cout << "===================================================\n";
        } else {
            std::cerr << "Invalid weather data received.\n";
        }
    } catch (json::parse_error& e) {
        std::cerr << "JSON Parse Error: " << e.what() << std::endl;
    }
}

int main() {
    std::string city, apiKey;

    std::cout << "Enter city name: ";
    std::getline(std::cin, city);

    std::cout << "Enter your OpenWeatherMap API key: ";
    std::getline(std::cin, apiKey);

    if (city.empty() || apiKey.empty()) {
        std::cerr << "City and API key cannot be empty.\n";
        return 1;
    }

    std::string weatherData = fetchWeatherData(city, apiKey);

    if (!weatherData.empty()) {
        displayWeather(weatherData);
    } else {
        std::cerr << "Failed to fetch weather data.\n";
    }

    return 0;
}
Example:-
OUTPUT-
Enter city name: London
Enter your OpenWeatherMap API key: YOUR_API_KEY

================ WEATHER DASHBOARD ================
City: London
Temperature: 18.5 °C
Feels Like: 17.9 °C
Humidity: 72 %
Condition: scattered clouds
