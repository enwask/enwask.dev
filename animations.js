// Whether we think the user is on a mobile device.
const is_mobile = window.matchMedia(
  "only screen and (max-width: 760px)",
).matches;

// Whether we should do animations, based on user preference.
const do_animations = window.matchMedia(
  "(prefers-reduced-motion: no-preference)",
).matches;

// All elements to apply the font weight animation to.
const font_weight_animation_targets = document.querySelectorAll(".works-title");

/**
 * Gets the vertical offset of the mouse from the element.
 * Anything within the element's bounding box is 0; above is negative, below is positive.
 */
function get_mouse_vertical_offset(element, event, padding = 0) {
  let rect = element.getBoundingClientRect();
  let y = event.clientY;

  if (y < rect.top - padding) return (y - (rect.top - padding)) / (rect.top - padding);
  if (y > rect.bottom + padding) return (y - (rect.bottom + padding)) / (window.innerHeight - rect.bottom - padding);
  return 0;
}
function get_mouse_vertical_offset_percent(element, event) {
  let unbiased = get_mouse_vertical_offset(element, event, padding = 12);
  return 1 - Math.pow(1 - Math.abs(unbiased), 4);
}

/**
 * Sets the font weight of an element based on a percentage from 0 to 1.
 */
function set_font_weight(element, weight_percent) {
  let weight = 200 + Math.round(weight_percent * 700);
  element.style.setProperty("--wght", weight);
}

/**
 * Mobile scroll listener.
 * Assigns font weight based on distances of elements from the center of the screen.
 */
function on_scroll_mobile(event) {
  let center_y = window.innerHeight / 2;

  font_weight_animation_targets.forEach((element) => {
    let rect = element.getBoundingClientRect();
    let element_center_y = rect.top + rect.height / 2;

    // If it's at the center or above, it gets full font weight
    if (element_center_y <= center_y) {
      set_font_weight(element, 1);
      return;
    }

    // Otherwise, set weight inversely proportional to distance from center
    let weight_percent = (element_center_y - center_y) / center_y;
    weight_percent = Math.max(0, Math.min(1, weight_percent));

    set_font_weight(element, weight_percent);
  });
}

/**
 * Desktop mousemove listener.
 * Assigns font weight based on mouse vertical offset from each element.
 */
function on_mousemove_desktop(event) {
  font_weight_animation_targets.forEach((element) => {
    let offset_percent = get_mouse_vertical_offset_percent(element, event);

    let weight_percent = 1 - Math.abs(offset_percent);
    weight_percent = Math.max(0, Math.min(1, weight_percent));

    set_font_weight(element, weight_percent);
  });
}

if (do_animations) {
  if (is_mobile) {
    // Mobile: scroll listener
    window.addEventListener("scroll", on_scroll_mobile);
  } else {
    // Desktop: mousemove listener
    window.addEventListener("mousemove", on_mousemove_desktop);
  }
}
