using InstagramApiSharp.API;
using InstagramApiSharp.API.Builder;
using InstagramApiSharp.Classes;
using InstagramApiSharp.Logger;


namespace InstagramProfileClock
{
    internal class Program
    {
        private static UserSessionData user = new UserSessionData
        {
            UserName = "username",
            Password = "password"
        };
        public static IInstaApi api = InstaApiBuilder.CreateBuilder()
                .SetUser(user)
                .UseLogger(new DebugLogger(LogLevel.All))
                .SetRequestDelay(RequestDelay.FromSeconds(0, 1))
                .Build();

        static void Main(string[] args)
        {
            if (Login().Result)
            {
                Console.WriteLine("User logged in successfully!");
            }
            string oldPath = "";
            while (true)
            {
                if (oldPath != GetClockImagePath(oldPath))
                {
                    UpdateProfilePicture(GetClockImagePath(oldPath)).Wait();
                    Thread.Sleep(15000); // Wait for 1 minute}
                }
                else
                {
                    Thread.Sleep(15000);
                }
            }
        }
        private static async Task<bool> Login()
        {
            if (!api.IsUserAuthenticated)
            {
                // login
                Console.WriteLine($"Logging in as {user.UserName}");
                var logInResult = await api.LoginAsync();
                if (!logInResult.Succeeded)
                {
                    Console.WriteLine($"Unable to login: {logInResult.Info.Message}");
                    return false;
                }
            }
            return true;
        }
        private static async Task<bool> UpdateProfilePicture(string imgPath)
        {
            var imageBytes = File.ReadAllBytes(imgPath);
            var uploadPhotoResult = await api.AccountProcessor.ChangeProfilePictureAsync(imageBytes);

            if (uploadPhotoResult.Succeeded)
            {
                Console.WriteLine("Profile picture updated successfully.");
                return true;
            }
            else
            {
                Console.WriteLine($"Failed to update profile picture: {uploadPhotoResult.Info.Message}");
                return false;
            }
        }
        private static async Task<bool> DeleteProfilePicture()
        {
            var deleteProfileResult = await api.AccountProcessor.RemoveProfilePictureAsync();

            if (deleteProfileResult.Succeeded)
            {
                Console.WriteLine("Profile picture deleted successfully.");
                return true;
            }
            else
            {
                Console.WriteLine($"Failed to delete profile picture: {deleteProfileResult.Info.Message}");
                return false;
            }
        }
        private static string GetClockImagePath(string oldPath)
        {
            DateTime now = DateTime.Now;
            string formattedTime = now.ToString("hhmm"); // Example: "1015" for 10:15 AM
            string directoryPath = @"C:\Users\TuanAnh\Desktop\clock\"; // Replace with your actual directory path
            string imagePath = Path.Combine(directoryPath, $"{formattedTime}.jpg");
            oldPath = imagePath;
            return imagePath;
        }
    }
}
