using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace AiroRobloxBuilder;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        AddMessage("builder", "what are we building?");
    }

    private void Send_Click(object sender, RoutedEventArgs e)
    {
        var text = PromptBox.Text.Trim();
        if (string.IsNullOrWhiteSpace(text) || text.StartsWith("describe your game"))
            return;
        AddMessage("you", text);
        PromptBox.Clear();
        AddMessage("builder", text.StartsWith("/plan")
            ? "planning is ready for the native core. the planner will turn this request into tasks once the orchestrator is connected."
            : "request accepted. routing is ready for the orchestrator and agent runtime.");
    }

    private void AddMessage(string speaker, string text)
    {
        var panel = new StackPanel { Margin = new Thickness(0, 0, 0, 16) };
        panel.Children.Add(new TextBlock { Text = speaker, FontWeight = FontWeights.SemiBold, Foreground = speaker == "you" ? Brushes.LightSkyBlue : Brushes.LightGreen });
        panel.Children.Add(new TextBlock { Text = text, TextWrapping = TextWrapping.Wrap, FontSize = 15, Margin = new Thickness(0, 4, 0, 0) });
        ChatMessages.Children.Add(panel);
    }
}