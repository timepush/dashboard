export function isTouchBased() {
  return window.matchMedia("(pointer: coarse)").matches;
}
