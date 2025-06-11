// Renders the trade calendar using FullCalendar and displays daily PnL

document.addEventListener('DOMContentLoaded', function () {
  const calendarEl = document.getElementById('calendar');
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    height: 'auto',
    events: window.dailyPnlData,
    eventContent: function(arg) {
      // Only render the number if there is a title 
      if (!arg.event.title) return { domNodes: [] };

      // Parse PnL value and determine color scheme
      const pnl = parseFloat(arg.event.title.replace(/[^0-9.-]/g, ''));
      const isProfit = pnl >= 0;
      const color = isProfit ? "#19e37d" : "#ff4d6d"; // green for profit, red for loss
      const shadow = isProfit
        ? "0 2px 12px #19e37d33, 0 1px 0 #101014"
        : "0 2px 12px #ff4d6d33, 0 1px 0 #101014";
      const bg = isProfit
        ? "rgba(25,227,125,0.10)"
        : "rgba(255,77,109,0.10)";

      // Create styled div for event content
      const div = document.createElement('div');
      div.style.display = 'flex';
      div.style.alignItems = 'center';
      div.style.justifyContent = 'center';
      div.style.height = '100%';
      div.style.width = '100%';
      div.style.fontSize = '2.6rem';
      div.style.fontWeight = '900';
      div.style.borderRadius = '10px';
      div.style.background = bg;
      div.style.color = color;
      div.style.boxShadow = shadow;
      div.style.margin = '0';
      div.style.padding = '0';
      div.style.letterSpacing = '0.5px';
      div.style.transition = 'color 0.2s, box-shadow 0.2s, background 0.2s';
      div.style.userSelect = 'none';
      div.textContent = arg.event.title;
      return { domNodes: [div] };
    },
  });
  calendar.render();
});