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

    private void Send_Click(object sender, RoutedEventArgs e) => SendPrompt();

    private void PromptBox_KeyDown(object sender, System.Windows.Input.KeyEventArgs e)
    {
        if (e.Key == System.Windows.Input.Key.Enter && !System.Windows.Input.Keyboard.Modifiers.HasFlag(System.Windows.Input.ModifierKeys.Shift))
        {
            e.Handled = true;
            SendPrompt();
        }
    }

    private void SendPrompt()
    {
        var text = PromptBox.Text.Trim();
        if (string.IsNullOrWhiteSpace(text) || text.StartsWith("describe your game"))
            return;

        AddMessage("you", text);
        PromptBox.Clear();

        var response = text.StartsWith("/plan") ? "planning request queued. the planner will turn this into a living task graph."
            : text.StartsWith("/tasks") ? "task view is ready. live task state will appear when the orchestrator is connected."
            : text.StartsWith("/test") ? "test request queued. the testing agent will report results here."
            : text.StartsWith("/fix") ? "repair request queued. diagnostics will be routed through the repair agent."
            : "request accepted. the native shell is ready to hand this to the orchestrator.";

        AddMessage("builder", response);
    }

    private void AddMessage(string speaker, string text)
    {
        var panel = new StackPanel { Margin = new Thickness(0, 0, 0, 18) };
        panel.Children.Add(new TextBlock { Text = speaker, FontWeight = FontWeights.SemiBold, Foreground = speaker == "you" ? Brushes.LightSkyBlue : Brushes.LightGreen });
        panel.Children.Add(new TextBlock { Text = text, TextWrapping = TextWrapping.Wrap, FontSize = 15, Margin = new Thickness(0, 4, 0, 0) });
        ChatMessages.Children.Add(panel);
    }
}