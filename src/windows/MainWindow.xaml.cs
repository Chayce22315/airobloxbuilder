using System.Windows;
using System.Windows.Controls;

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
        if (string.IsNullOrWhiteSpace(text))
            return;

        AddMessage("you", text);
        PromptBox.Clear();
        AddMessage("builder", "request received. the orchestrator is not connected yet, but the native shell is alive.");
    }

    private void AddMessage(string speaker, string text)
    {
        ChatMessages.Children.Add(new TextBlock
        {
            Text = $"{speaker}: {text}",
            TextWrapping = TextWrapping.Wrap,
            Margin = new Thickness(0, 0, 0, 14),
            FontSize = 16
        });
    }
}
