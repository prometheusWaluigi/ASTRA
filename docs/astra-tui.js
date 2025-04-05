#!/usr/bin/env node

/**
 * ASTRA TUI - Terminal interface for Archetypal Spacetime Tensor Resonance Architecture
 * A Neovim-inspired interface for consciousness field visualization
 */

const blessed = require('blessed');
const contrib = require('blessed-contrib');
const chalk = require('chalk');
const { execSync } = require('child_process');

// ASCII art logo
const LOGO = `
   █████╗ ███████╗████████╗██████╗  █████╗ 
  ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗
  ███████║███████╗   ██║   ██████╔╝███████║
  ██╔══██║╚════██║   ██║   ██╔══██╗██╔══██║
  ██║  ██║███████║   ██║   ██║  ██║██║  ██║
  ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
  Ψ-Field Topology Interface ${chalk.dim('v1.0.0')}
`;

class ASTRA_TUI {
  constructor() {
    this.screen = blessed.screen({
      smartCSR: true,
      title: 'ASTRA Terminal Interface',
      cursor: {
        artificial: true,
        shape: 'line',
        blink: true
      }
    });
    
    this.loading = true;
    this.mode = 'NORMAL';
    this.fieldData = this.generateFieldData();
    this.symmetryGraph = this.generateSymmetryData();
    this.cmdBuffer = '';
    
    this.setupLayout();
    this.setupBindings();
    this.render();
    
    // Simulate loading
    setTimeout(() => {
      this.loading = false;
      this.renderStatusLine();
      this.render();
    }, 2000);
  }
  
  setupLayout() {
    // Main layout grid
    this.grid = new contrib.grid({ 
      rows: 12, 
      cols: 12, 
      screen: this.screen 
    });
    
    // Header
    this.header = blessed.box({
      top: 0,
      left: 0,
      width: '100%',
      height: 7,
      content: chalk.cyan(LOGO),
      tags: true,
      style: {
        fg: 'cyan'
      }
    });
    
    // Field visualization
    this.fieldMap = this.grid.set(7, 0, 8, 8, contrib.map, {
      label: ' Ψ-Field Topology ',
      style: {
        fg: 'cyan',
        border: { fg: 'cyan' }
      }
    });
    
    // Narrative Timeline
    this.timeline = this.grid.set(15, 0, 3, 8, contrib.line, {
      style: {
        line: 'cyan',
        text: 'white',
        baseline: 'white'
      },
      xLabelPadding: 3,
      xPadding: 5,
      showLegend: true,
      legend: { width: 20 },
      wholeNumbersOnly: false,
      label: ' Temporal Symmetry '
    });
    
    // Command Palette 
    this.cmdPalette = this.grid.set(7, 8, 11, 4, contrib.log, {
      fg: 'green',
      selectedFg: 'green',
      label: ' Command Mode ',
      tags: true
    });
    
    // Status line
    this.status = blessed.box({
      bottom: 0,
      left: 0,
      width: '100%',
      height: 1,
      style: {
        fg: 'black',
        bg: 'cyan'
      }
    });
    
    // Add all elements
    this.screen.append(this.header);
    this.screen.append(this.status);
    
    // Initial data
    this.renderFieldMap();
    this.renderTimeline();
    this.renderCmdPalette();
    this.renderStatusLine();
  }
  
  setupBindings() {
    // Neovim-style bindings
    this.screen.key(['C-c', 'q'], () => process.exit(0));
    this.screen.key(['escape'], () => this.setNormalMode());
    this.screen.key([':'], () => this.setCommandMode());
    this.screen.key(['C-n'], () => this.nextView());
    this.screen.key(['C-p'], () => this.prevView());
    this.screen.key(['j', 'down'], () => this.scrollDown());
    this.screen.key(['k', 'up'], () => this.scrollUp());
    this.screen.key(['h', 'left'], () => this.decreaseValue());
    this.screen.key(['l', 'right'], () => this.increaseValue());
    
    // Command mode handling
    this.screen.key(['return'], () => {
      if (this.mode === 'COMMAND') {
        this.executeCommand(this.cmdBuffer);
        this.cmdBuffer = '';
        this.setNormalMode();
      }
    });
    
    // When in command mode, capture typed characters
    this.screen.on('keypress', (ch, key) => {
      if (this.mode === 'COMMAND' && !key.ctrl && ch && key.name !== 'return' && key.name !== 'escape') {
        if (key.name === 'backspace') {
          this.cmdBuffer = this.cmdBuffer.slice(0, -1);
        } else {
          this.cmdBuffer += ch || '';
        }
        this.renderStatusLine();
        this.render();
      }
    });
  }
  
  setNormalMode() {
    this.mode = 'NORMAL';
    this.cmdBuffer = '';
    this.renderStatusLine();
    this.render();
  }
  
  setCommandMode() {
    this.mode = 'COMMAND';
    this.cmdBuffer = '';
    this.renderStatusLine();
    this.render();
  }
  
  executeCommand(cmd) {
    cmd = cmd.trim();
    
    if (cmd === 'q' || cmd === 'quit') {
      process.exit(0);
    } else if (cmd === 'help') {
      this.showHelp();
    } else if (cmd.startsWith('set ts=')) {
      // Set temporal symmetry value
      const value = parseFloat(cmd.replace('set ts=', ''));
      if (!isNaN(value) && value >= 0 && value <= 1) {
        this.symmetryValue = value;
        this.updateSymmetryGraph();
      }
    } else if (cmd === 'gen' || cmd === 'generate') {
      // Regenerate field
      this.fieldData = this.generateFieldData();
      this.renderFieldMap();
    } else {
      this.cmdPalette.log(chalk.red(`Unknown command: ${cmd}`));
    }
  }
  
  showHelp() {
    const help = [
      chalk.cyan('-- ASTRA TUI Commands --'),
      ':quit or :q    Exit the application',
      ':help          Show this help message',
      ':set ts=0.5    Set temporal symmetry value (0-1)',
      ':generate      Generate new field data',
      '',
      chalk.cyan('-- Keyboard Shortcuts --'),
      'Ctrl+n/p       Next/previous view',
      'j/k            Scroll down/up',
      'h/l            Decrease/increase value',
      'Esc            Return to normal mode',
      ':              Enter command mode'
    ];
    
    help.forEach(line => this.cmdPalette.log(line));
  }
  
  scrollDown() {
    // Implement scrolling logic based on active view
  }
  
  scrollUp() {
    // Implement scrolling logic based on active view
  }
  
  increaseValue() {
    if (this.symmetryValue < 1) {
      this.symmetryValue += 0.05;
      if (this.symmetryValue > 1) this.symmetryValue = 1;
      this.updateSymmetryGraph();
    }
  }
  
  decreaseValue() {
    if (this.symmetryValue > 0) {
      this.symmetryValue -= 0.05;
      if (this.symmetryValue < 0) this.symmetryValue = 0;
      this.updateSymmetryGraph();
    }
  }
  
  nextView() {
    // Cycle through available views
    this.cmdPalette.log(chalk.cyan('Switched to next view'));
  }
  
  prevView() {
    // Cycle through available views in reverse
    this.cmdPalette.log(chalk.cyan('Switched to previous view'));
  }
  
  generateFieldData() {
    // Generate fictional topology data
    const data = {};
    const markers = [];
    
    // Create markers for significant points in consciousness field
    for (let i = 0; i < 10; i++) {
      const lat = (Math.random() * 180) - 90;
      const lon = (Math.random() * 360) - 180;
      const color = ['red', 'yellow', 'green', 'blue', 'cyan', 'magenta'][Math.floor(Math.random() * 6)];
      
      markers.push({ 
        lat, 
        lon, 
        color, 
        char: 'ψ' 
      });
    }
    
    return markers;
  }
  
  generateSymmetryData() {
    // Default symmetry value (0-1)
    this.symmetryValue = 0.5;
    
    // Generate time series data
    const data = {
      x: Array.from({length: 50}, (_, i) => i),
      y: Array.from({length: 50}, () => Math.random() * 100 - 50)
    };
    
    return data;
  }
  
  updateSymmetryGraph() {
    // Update the graph based on symmetry value
    const modulation = Math.sin(this.symmetryValue * Math.PI * 2);
    
    // Update y values based on symmetry
    this.symmetryGraph.y = this.symmetryGraph.y.map((v, i) => {
      return v * modulation + (Math.sin(i/5) * 20);
    });
    
    this.renderTimeline();
    this.render();
  }
  
  renderFieldMap() {
    // Clear existing markers
    this.fieldMap.clearMarkers();
    
    // Add new markers
    this.fieldData.forEach(marker => {
      this.fieldMap.addMarker({
        lat: marker.lat,
        lon: marker.lon,
        color: marker.color,
        char: marker.char
      });
    });
  }
  
  renderTimeline() {
    const data = [{
      title: 'Temporal Symmetry',
      x: this.symmetryGraph.x,
      y: this.symmetryGraph.y,
      style: {
        line: 'cyan'
      }
    }];
    
    this.timeline.setData(data);
  }
  
  renderCmdPalette() {
    if (this.loading) {
      this.cmdPalette.log(chalk.cyan('Loading ASTRA Ψ-Field interface...'));
    } else if (this.cmdPalette.getLines().length === 0) {
      this.cmdPalette.log(chalk.cyan('-- ASTRA Terminal Interface --'));
      this.cmdPalette.log('Welcome to the consciousness field visualizer');
      this.cmdPalette.log('Press : to enter command mode or ? for help');
      this.cmdPalette.log('');
      this.cmdPalette.log(`${chalk.green('Current Betti numbers:')} β₀=3, β₁=2, β₂=1`);
      this.cmdPalette.log(`${chalk.green('Ricci Curvature:')} -0.112`);
      this.cmdPalette.log(`${chalk.green('Symmetry Value:')} ${this.symmetryValue.toFixed(2)}`);
    }
  }
  
  renderStatusLine() {
    let content = '';
    
    if (this.loading) {
      content = chalk.black.bgYellow(' LOADING ');
    } else if (this.mode === 'NORMAL') {
      content = chalk.black.bgCyan(' NORMAL ') + ' ASTRA TUI v1.0.0 | Ψ-Field Explorer | Symmetry: ' + this.symmetryValue.toFixed(2);
    } else if (this.mode === 'COMMAND') {
      content = chalk.black.bgYellow(' COMMAND ') + ' :' + this.cmdBuffer;
    }
    
    this.status.setContent(content);
  }
  
  render() {
    this.screen.render();
  }
}

// Initialize and start TUI
try {
  new ASTRA_TUI();
} catch (e) {
  console.error('Error initializing ASTRA TUI:', e);
  process.exit(1);
}
