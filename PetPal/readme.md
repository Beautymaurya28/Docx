This is a fantastic and incredibly well-structured project plan. I'm ready to build this with you.



-----

### 1\. Prerequisites & Environment Setup

First, you need to have Node.js (LTS version is recommended) and the Ionic CLI installed on your system.

If you don't have the Ionic CLI, install it globally:

```bash
npm install -g @ionic/cli
```

You will also need a code editor, such as [VS Code](https://code.visualstudio.com/).

### 2\. Project & Folder Creation

Now, let's create the new Ionic + Angular project.

1.  Open your terminal and run the following command. We'll use the `blank` template to have a clean slate for our custom design.

    ```bash
    ionic start PetPal blank --type=angular --capacitor
    ```

      * `PetPal`: This is your project's name.
      * `blank`: The template we are using.
      * `--type=angular`: Specifies we are using the Angular framework.
      * `--capacitor`: Includes the Capacitor native runtime, which we'll need for mobile features like the Vets Map.

2.  When prompted, `Use @ionic/angular package?`, select **Yes**.

3.  Once it's finished, navigate into your new project directory:

    ```bash
    cd PetPal
    ```

4.  (Optional) Open the project in VS Code:

    ```bash
    code .
    ```

### 3\. Key Theme Files

Inside your `src` folder, we will primarily work with these files for Phase 0:

  * `src/theme/variables.scss`: This is where we will define your global color palette (the sky-blue CTA, etc.) and other variables like border-radius.
  * `src/global.scss`: We'll use this to apply global styles, like the background gradient, font, and custom button styles.
  * `src/app/app.component.html` & `src/app/app.component.scss`: This is the root component of your app. We'll add the persistent floating chatbot button here so it appears on every page.

-----

### 4\. Applying the Global Theme

Let's implement the design tokens from your prompt.

#### Step 1: Set the Global Background Gradient

Open `src/global.scss` and add the following code. This will apply your dark gradient to the main content area of every page.

```scss
/* In src/global.scss */

/* Import the Inter font (a clean sans-serif) */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

body {
  /* Apply the clean sans font globally */
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, 
               "Helvetica Neue", Arial, sans-serif;
}

/* Apply the global background gradient */
ion-content {
  --background: linear-gradient(160deg, #1f2d3a 0%, #1a1a2e 100%);
}
```

#### Step 2: Define Color Palette & Variables

Open `src/theme/variables.scss`. We need to override Ionic's default colors with your `PetPal` theme.

Find the `:root` selector and replace its contents with this. We are setting `primary` to your sky-blue CTA color and ensuring the dark theme text is white.

```scss
/* In src/theme/variables.scss */
:root {
  /** Ionic CSS Variables **/
  
  /* Set the default text color for dark mode */
  --ion-text-color: #ffffff;
  --ion-text-color-rgb: 255, 255, 255;

  /* * PRIMARY (CTA) COLOR 
   * Used for: Main buttons, links, toggles, floating button
   */
  --ion-color-primary: #29b6f6;
  --ion-color-primary-rgb: 41, 182, 246;
  --ion-color-primary-contrast: #000000;
  --ion-color-primary-contrast-rgb: 0, 0, 0;
  --ion-color-primary-shade: #24a0d9;
  --ion-color-primary-tint: #3ebcf7;

  /* * Dark theme color overrides
   * (Ensures backgrounds are dark and text is light) 
   */
  .ios,
  .md {
    --ion-background-color: #1a1a2e;
    --ion-background-color-rgb: 26, 26, 46;

    --ion-text-color: #ffffff;
    --ion-text-color-rgb: 255, 255, 255;

    --ion-color-step-50: #2a2a40;
    --ion-color-step-100: #33334f;
    /* ...and so on */

    /* For Phase 2: Translucent cards */
    --ion-item-background: rgba(255, 255, 255, 0.08);
    --ion-card-background: rgba(255, 255, 255, 0.08);
  }
}
```

#### Step 3: Style Global Components (Cards & Buttons)

Now, let's add the global styles for cards (rounded radius, shadow) and your secondary outline button.

Add this code to the bottom of `src/global.scss`:

```scss
/* In src/global.scss (at the bottom) */

/*
 * Global Card Styling
 * (For Phase 2)
 */
ion-card {
  /* Use the variable we defined in variables.scss */
  --background: var(--ion-card-background);
  
  border-radius: 14px;
  
  /* Your 2xl soft shadow, adjusted for a dark background */
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.15);
}

/* * Button Styling
 */

/* * Primary buttons (filled sky-blue)
 * This is automatic! Just add color="primary" to an <ion-button>
 * e.g. <ion-button color="primary">Login</ion-button>
 */

/* * Secondary buttons (white outline)
 * We'll create a custom class for this.
 */
ion-button.button-outline-white {
  --background: transparent;
  --border-color: #ffffff;
  --border-width: 1px;
  --border-style: solid;
  --color: #ffffff;
  --color-activated: #eeeeee;
  
  /* Ripple effect color */
  --ripple-color: #ffffff;
}
```

-----

### 5\. Add the Persistent Chatbot Button

This is a global UI element, so it belongs in `src/app/app.component.html`.

1.  **Open `src/app/app.component.html`**
    Replace the entire file contents with this. We are adding an `<ion-fab>` (Floating Action Button) which will contain our pet icon.

    ```html
    <ion-app>
      <ion-router-outlet></ion-router-outlet>

      <ion-fab vertical="bottom" horizontal="end" slot="fixed">
        <ion-fab-button color="primary" (click)="openChat()">
          <ion-icon name="chatbubbles-outline"></ion-icon>
        </ion-fab-button>
      </ion-fab>
    </ion-app>
    ```

2.  **Open `src/app/app.component.scss`**
    Add this style to make the button 64px as requested.

    ```scss
    ion-fab-button {
      width: 64px;
      height: 64px;
    }
    ```

3.  **Open `src/app/app.component.ts`**
    Add the `openChat()` method. For now, it will just log to the console. In Phase 4, we will make this open the chat drawer.

    ```typescript
    import { Component } from '@angular/core';

    @Component({
      selector: 'app-root',
      templateUrl: 'app.component.html',
      styleUrls: ['app.component.scss'],
    })
    export class AppComponent {
      constructor() {}

      openChat() {
        // TODO: (Phase 4) Implement chat drawer logic
        console.log('Open chat drawer');
      }
    }
    ```

-----

### 6\. Verify Your Work

Let's run the app and see our theme in action.

1.  Run `ionic serve` in your terminal:

    ```bash
    ionic serve
    ```

    This will open the app in your browser, likely at `http://localhost:8100`.

2.  You should see a blank page with your dark gradient background and the sky-blue chatbot button in the bottom-right corner.

3.  **Test the styles:** Open `src/app/home/home.page.html` and add some test elements inside the `<ion-content>` tag:

    ```html
    <ion-header [translucent]="true">
      <ion-toolbar color="primary">
        <ion-title>PetPal Theme Test</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content [fullscreen]="true">
      <ion-header collapse="condense">
        <ion-toolbar>
          <ion-title size="large">PetPal Test</ion-title>
        </ion-toolbar>
      </ion-header>

      <div style="padding: 16px;">
        <h1>Welcome to PetPal</h1>
        <p>This text should be white or light gray.</p>

        <h3>Buttons</h3>
        <ion-button color="primary">Primary CTA (Filled)</ion-button>
        <ion-button class="button-outline-white">Secondary (Outline)</ion-button>

        <h3>Card (for Phase 2)</h3>
        <ion-card>
          <ion-card-header>
            <ion-card-title>Test Card</ion-card-title>
          </ion-card-header>
          <ion-card-content>
            This card should be semi-translucent with rounded corners and a soft shadow.
          </ion-card-content>
        </ion-card>
      </div>

    </ion-content>
    ```

If you see your dark gradient, the sky-blue button, the white text, and the styled card, then **Phase 0 is complete\!**

-----

Let me know when you have this running, and we'll move on to **Phase 1: Authentication & Flow** (building the Login/Signup pages and the backend auth endpoints).







