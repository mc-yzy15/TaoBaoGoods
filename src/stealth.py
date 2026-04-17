from __future__ import annotations

import random
import time
from typing import Any

import selenium.webdriver.common.action_chains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth as base_stealth

from src.config import AppConfig


def _human_delay(min_sec: float = 0.05, max_sec: float = 0.15) -> float:
    return random.uniform(min_sec, max_sec)


def _stealth_chrome(
    driver: webdriver.Chrome,
    vendor: str = "Google",
    fix_clr: bool = True,
    fix_chrome: bool = True,
    fix_webgl: bool = True,
    fix_webgl2: bool = True,
    fix_canvas: bool = True,
    fix_webgl_params: bool = True,
    fix_history: bool = True,
    fix_pdf: bool = True,
    fix_media: bool = True,
    fix_permissions: bool = True,
    fix_geolocation: bool = True,
    fix_language: bool = True,
    fix_proxy: bool = True,
    fix_dnt: bool = True,
    fix_platform: bool = True,
    fix_hardware_concurrency: bool = True,
    fix_device_memory: bool = True,
    fix_screen_size: bool = True,
) -> None:
    has_navigator_webdriver = """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined,
        configurable: true,
        enumerable: true
    });
    delete navigator.webdriver;
    try {
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    } catch (e) {}
    """

    has_webgl = """
    const dummyContext = {};
    const origGetContext = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(contextType, contextAttributes) {
        if (contextType === 'webgl' || contextType === 'webgl2' || contextType === 'experimental-webgl') {
            try {
                const ctx = origGetContext.call(this, contextType, contextAttributes);
                if (!ctx) return dummyContext;
                const originalGetParameter = ctx.getParameter;
                ctx.getParameter = function(param) {
                    if (param === 37445) return 'Intel Inc.';
                    if (param === 37446) return 'Intel Iris OpenGL Engine';
                    if (param === 3412) return 0;
                    if (param === 3413) return 0;
                    if (param === 3414) return 1;
                    if (param === 3415) return 8;
                    if (param === 7936) return 'Intel Iris OpenGL Engine';
                    if (param === 7937) return 'Intel Iris OpenGL Engine';
                    if (param === 7938) return 255;
                    if (param === 7939) return 218762004;
                    if (param === 7940) return 942810852;
                    if (param === 7941) return 897589952;
                    if (param === 7944) return 131072;
                    if (param === 7945) return 0;
                    if (param === 7936 + 1) return 1;
                    if (param === 7936 + 2) return 24;
                    if (param === 7936 + 3) return 8;
                    if (param === 7936 + 4) return 24;
                    if (param === 7936 + 5) return 8;
                    if (param === 7936 + 6) return 0;
                    if (param === 7936 + 7) return 0;
                    if (param === 7936 + 8) return 0;
                    if (param === 7936 + 9) return 0;
                    if (param === 7936 + 10) return 0;
                    if (param === 7936 + 11) return 0;
                    if (param === 7936 + 12) return 0;
                    if (param === 7936 + 13) return 0;
                    if (param === 7936 + 14) return 0;
                    if (param === 7936 + 15) return 0;
                    if (param === 7936 + 16) return 1;
                    if (param === 7936 + 17) return 16384;
                    if (param === 7936 + 18) return 0;
                    if (param === 7936 + 19) return 16384;
                    if (param === 7936 + 20) return 0;
                    if (param === 7936 + 21) return 4;
                    if (param === 7936 + 22) return 0;
                    if (param === 7936 + 23) return 0;
                    if (param === 7936 + 24) return 0;
                    if (param === 7936 + 25) return 0;
                    if (param === 7936 + 26) return 1;
                    if (param === 7936 + 27) return 0;
                    if (param === 7936 + 28) return 0;
                    if (param === 7936 + 29) return 16384;
                    if (param === 7936 + 30) return 0;
                    if (param === 7936 + 31) return 0;
                    if (param === 7936 + 32) return 0;
                    if (param === 7936 + 33) return 0;
                    if (param === 7936 + 34) return 0;
                    if (param === 7936 + 35) return 0;
                    if (param === 7936 + 36) return 0;
                    if (param === 7936 + 37) return 1;
                    if (param === 7936 + 38) return 0;
                    if (param === 7936 + 39) return 1;
                    if (param === 7936 + 40) return 0;
                    if (param === 7936 + 41) return 0;
                    if (param === 7936 + 42) return 0;
                    if (param === 7936 + 43) return 0;
                    if (param === 7936 + 44) return 0;
                    if (param === 7936 + 45) return 0;
                    if (param === 7936 + 46) return 0;
                    if (param === 7936 + 47) return 0;
                    if (param === 7936 + 48) return 0;
                    if (param === 7936 + 49) return 0;
                    if (param === 7936 + 50) return 0;
                    if (param === 7936 + 51) return 0;
                    if (param === 7936 + 52) return 0;
                    if (param === 7936 + 53) return 1;
                    if (param === 7936 + 54) return 1;
                    if (param === 7936 + 55) return 1;
                    if (param === 7936 + 56) return 0;
                    if (param === 7936 + 57) return 0;
                    if (param === 7936 + 58) return 0;
                    if (param === 7936 + 59) return 0;
                    if (param === 7936 + 60) return 0;
                    if (param === 7936 + 61) return 0;
                    if (param === 7936 + 62) return 0;
                    if (param === 7936 + 63) return 0;
                    if (param === 7936 + 64) return 0;
                    if (param === 7936 + 65) return 0;
                    if (param === 7936 + 66) return 0;
                    if (param === 7936 + 67) return 0;
                    if (param === 7936 + 68) return 0;
                    if (param === 7936 + 69) return 0;
                    if (param === 7936 + 70) return 0;
                    if (param === 7936 + 71) return 0;
                    if (param === 7936 + 72) return 0;
                    if (param === 7936 + 73) return 0;
                    if (param === 7936 + 74) return 0;
                    if (param === 7936 + 75) return 0;
                    if (param === 7936 + 76) return 0;
                    if (param === 7936 + 77) return 1;
                    if (param === 7936 + 78) return 0;
                    if (param === 7936 + 79) return 0;
                    if (param === 7936 + 80) return 1;
                    if (param === 7936 + 81) return 0;
                    if (param === 7936 + 82) return 0;
                    if (param === 7936 + 83) return 0;
                    if (param === 7936 + 84) return 0;
                    if (param === 7936 + 85) return 0;
                    if (param === 7936 + 86) return 0;
                    if (param === 7936 + 87) return 0;
                    if (param === 7936 + 88) return 0;
                    if (param === 7936 + 89) return 0;
                    if (param === 7936 + 90) return 0;
                    if (param === 7936 + 91) return 0;
                    if (param === 7936 + 92) return 0;
                    if (param === 7936 + 93) return 0;
                    if (param === 7936 + 94) return 0;
                    if (param === 7936 + 95) return 0;
                    if (param === 7936 + 96) return 0;
                    if (param === 7936 + 97) return 0;
                    if (param === 7936 + 98) return 0;
                    if (param === 7936 + 99) return 0;
                    if (param === 7936 + 100) return 0;
                    if (param === 7936 + 101) return 0;
                    if (param === 7936 + 102) return 0;
                    if (param === 7936 + 103) return 0;
                    if (param === 7936 + 104) return 0;
                    if (param === 7936 + 105) return 0;
                    if (param === 7936 + 106) return 0;
                    if (param === 7936 + 107) return 0;
                    if (param === 7936 + 108) return 0;
                    if (param === 7936 + 109) return 0;
                    if (param === 7936 + 110) return 0;
                    if (param === 7936 + 111) return 0;
                    if (param === 7936 + 112) return 0;
                    if (param === 7936 + 113) return 0;
                    if (param === 7936 + 114) return 0;
                    if (param === 7936 + 115) return 0;
                    if (param === 7936 + 116) return 0;
                    if (param === 7936 + 117) return 0;
                    if (param === 7936 + 118) return 0;
                    if (param === 7936 + 119) return 0;
                    if (param === 7936 + 120) return 0;
                    if (param === 7936 + 121) return 0;
                    if (param === 7936 + 122) return 0;
                    if (param === 7936 + 123) return 0;
                    if (param === 7936 + 124) return 0;
                    if (param === 7936 + 125) return 0;
                    if (param === 7936 + 126) return 0;
                    if (param === 7936 + 127) return 0;
                    if (param === 7936 + 128) return 0;
                    if (param === 7936 + 129) return 0;
                    if (param === 7936 + 130) return 0;
                    if (param === 7936 + 131) return 0;
                    if (param === 7936 + 132) return 0;
                    if (param === 7936 + 133) return 0;
                    if (param === 7936 + 134) return 0;
                    if (param === 7936 + 135) return 0;
                    if (param === 7936 + 136) return 0;
                    if (param === 7936 + 137) return 0;
                    if (param === 7936 + 138) return 0;
                    if (param === 7936 + 139) return 0;
                    if (param === 7936 + 140) return 0;
                    if (param === 7936 + 141) return 0;
                    if (param === 7936 + 142) return 0;
                    if (param === 7936 + 143) return 0;
                    if (param === 7936 + 144) return 0;
                    if (param === 7936 + 145) return 0;
                    if (param === 7936 + 146) return 0;
                    if (param === 7936 + 147) return 0;
                    if (param === 7936 + 148) return 0;
                    if (param === 7936 + 149) return 0;
                    if (param === 7936 + 150) return 0;
                    if (param === 7936 + 151) return 0;
                    if (param === 7936 + 152) return 0;
                    if (param === 7936 + 153) return 0;
                    if (param === 7936 + 154) return 0;
                    if (param === 7936 + 155) return 0;
                    if (param === 7936 + 156) return 0;
                    if (param === 7936 + 157) return 0;
                    if (param === 7936 + 158) return 0;
                    if (param === 7936 + 159) return 0;
                    if (param === 7936 + 160) return 0;
                    if (param === 7936 + 161) return 0;
                    if (param === 7936 + 162) return 0;
                    if (param === 7936 + 163) return 0;
                    if (param === 7936 + 164) return 0;
                    if (param === 7936 + 165) return 0;
                    if (param === 7936 + 166) return 0;
                    if (param === 7936 + 167) return 0;
                    if (param === 7936 + 168) return 0;
                    if (param === 7936 + 169) return 0;
                    if (param === 7936 + 170) return 0;
                    if (param === 7936 + 171) return 0;
                    if (param === 7936 + 172) return 0;
                    if (param === 7936 + 173) return 0;
                    if (param === 7936 + 174) return 0;
                    if (param === 7936 + 175) return 0;
                    if (param === 7936 + 176) return 0;
                    if (param === 7936 + 177) return 0;
                    if (param === 7936 + 178) return 0;
                    if (param === 7936 + 179) return 0;
                    if (param === 7936 + 180) return 0;
                    if (param === 7936 + 181) return 0;
                    if (param === 7936 + 182) return 0;
                    if (param === 7936 + 183) return 0;
                    if (param === 7936 + 184) return 0;
                    if (param === 7936 + 185) return 0;
                    if (param === 7936 + 186) return 0;
                    if (param === 7936 + 187) return 0;
                    if (param === 7936 + 188) return 0;
                    if (param === 7936 + 189) return 0;
                    if (param === 7936 + 190) return 0;
                    if (param === 7936 + 191) return 0;
                    if (param === 7936 + 192) return 0;
                    if (param === 7936 + 193) return 0;
                    if (param === 7936 + 194) return 0;
                    if (param === 7936 + 195) return 0;
                    if (param === 7936 + 196) return 0;
                    if (param === 7936 + 197) return 0;
                    if (param === 7936 + 198) return 0;
                    if (param === 7936 + 199) return 0;
                    if (param === 7936 + 200) return 0;
                    if (param === 7936 + 201) return 0;
                    if (param === 7936 + 202) return 0;
                    if (param === 7936 + 203) return 0;
                    if (param === 7936 + 204) return 0;
                    if (param === 7936 + 205) return 0;
                    if (param === 7936 + 206) return 0;
                    if (param === 7936 + 207) return 0;
                    if (param === 7936 + 208) return 0;
                    if (param === 7936 + 209) return 0;
                    if (param === 7936 + 210) return 0;
                    if (param === 7936 + 211) return 0;
                    if (param === 7936 + 212) return 0;
                    if (param === 7936 + 213) return 0;
                    if (param === 7936 + 214) return 0;
                    if (param === 7936 + 215) return 0;
                    if (param === 7936 + 216) return 0;
                    if (param === 7936 + 217) return 0;
                    if (param === 7936 + 218) return 0;
                    if (param === 7936 + 219) return 0;
                    if (param === 7936 + 220) return 0;
                    if (param === 7936 + 221) return 0;
                    if (param === 7936 + 222) return 0;
                    if (param === 7936 + 223) return 0;
                    if (param === 7936 + 224) return 0;
                    if (param === 7936 + 225) return 0;
                    if (param === 7936 + 226) return 0;
                    if (param === 7936 + 227) return 0;
                    if (param === 7936 + 228) return 0;
                    if (param === 7936 + 229) return 0;
                    if (param === 7936 + 230) return 0;
                    if (param === 7936 + 231) return 0;
                    if (param === 7936 + 232) return 0;
                    if (param === 7936 + 233) return 0;
                    if (param === 7936 + 234) return 0;
                    if (param === 7936 + 235) return 0;
                    if (param === 7936 + 236) return 0;
                    if (param === 7936 + 237) return 0;
                    if (param === 7936 + 238) return 0;
                    if (param === 7936 + 239) return 0;
                    if (param === 7936 + 240) return 0;
                    if (param === 7936 + 241) return 0;
                    if (param === 7936 + 242) return 0;
                    if (param === 7936 + 243) return 0;
                    if (param === 7936 + 244) return 0;
                    if (param === 7936 + 245) return 0;
                    if (param === 7936 + 246) return 0;
                    if (param === 7936 + 247) return 0;
                    if (param === 7936 + 248) return 0;
                    if (param === 7936 + 249) return 0;
                    if (param === 7936 + 250) return 0;
                    if (param === 7936 + 251) return 0;
                    if (param === 7936 + 252) return 0;
                    if (param === 7936 + 253) return 0;
                    if (param === 7936 + 254) return 0;
                    if (param === 7936 + 255) return 0;
                    if (param === 7936 + 256) return 0;
                    if (param === 7936 + 257) return 0;
                    if (param === 7936 + 258) return 0;
                    if (param === 7936 + 259) return 0;
                    if (param === 7936 + 260) return 0;
                    if (param === 7936 + 261) return 0;
                    if (param === 7936 + 262) return 0;
                    if (param === 7936 + 263) return 0;
                    if (param === 7936 + 264) return 0;
                    if (param === 7936 + 265) return 0;
                    if (param === 7936 + 266) return 0;
                    if (param === 7936 + 267) return 0;
                    if (param === 7936 + 268) return 0;
                    if (param === 7936 + 269) return 0;
                    if (param === 7936 + 270) return 0;
                    if (param === 7936 + 271) return 0;
                    if (param === 7936 + 272) return 0;
                    if (param === 7936 + 273) return 0;
                    if (param === 7936 + 274) return 0;
                    if (param === 7936 + 275) return 0;
                    if (param === 7936 + 276) return 0;
                    if (param === 7936 + 277) return 0;
                    if (param === 7936 + 278) return 0;
                    if (param === 7936 + 279) return 0;
                    if (param === 7936 + 280) return 0;
                    if (param === 7936 + 281) return 0;
                    if (param === 7936 + 282) return 0;
                    if (param === 7936 + 283) return 0;
                    if (param === 7936 + 284) return 0;
                    if (param === 7936 + 285) return 0;
                    if (param === 7936 + 286) return 0;
                    if (param === 7936 + 287) return 0;
                    if (param === 7936 + 288) return 0;
                    if (param === 7936 + 289) return 0;
                    if (param === 7936 + 290) return 0;
                    if (param === 7936 + 291) return 0;
                    if (param === 7936 + 292) return 0;
                    if (param === 7936 + 293) return 0;
                    if (param === 7936 + 294) return 0;
                    if (param === 7936 + 295) return 0;
                    if (param === 7936 + 296) return 0;
                    if (param === 7936 + 297) return 0;
                    if (param === 7936 + 298) return 0;
                    if (param === 7936 + 299) return 0;
                    if (param === 7936 + 300) return 0;
                    if (param === 7936 + 301) return 0;
                    if (param === 7936 + 302) return 0;
                    if (param === 7936 + 303) return 0;
                    if (param === 7936 + 304) return 0;
                    if (param === 7936 + 305) return 0;
                    if (param === 7936 + 306) return 0;
                    if (param === 7936 + 307) return 0;
                    if (param === 7936 + 308) return 0;
                    if (param === 7936 + 309) return 0;
                    if (param === 7936 + 310) return 0;
                    if (param === 7936 + 311) return 0;
                    if (param === 7936 + 312) return 0;
                    if (param === 7936 + 313) return 0;
                    if (param === 7936 + 314) return 0;
                    if (param === 7936 + 315) return 0;
                    if (param === 7936 + 316) return 0;
                    if (param === 7936 + 317) return 0;
                    if (param === 7936 + 318) return 0;
                    if (param === 7936 + 319) return 0;
                    if (param === 7936 + 320) return 0;
                    if (param === 7936 + 321) return 0;
                    if (param === 7936 + 322) return 0;
                    if (param === 7936 + 323) return 0;
                    if (param === 7936 + 324) return 0;
                    if (param === 7936 + 325) return 0;
                    if (param === 7936 + 326) return 0;
                    if (param === 7936 + 327) return 0;
                    if (param === 7936 + 328) return 0;
                    if (param === 7936 + 329) return 0;
                    if (param === 7936 + 330) return 0;
                    if (param === 7936 + 331) return 0;
                    if (param === 7936 + 332) return 0;
                    if (param === 7936 + 333) return 0;
                    if (param === 7936 + 334) return 0;
                    if (param === 7936 + 335) return 0;
                    if (param === 7936 + 336) return 0;
                    if (param === 7936 + 337) return 0;
                    if (param === 7936 + 338) return 0;
                    if (param === 7936 + 339) return 0;
                    if (param === 7936 + 340) return 0;
                    if (param === 7936 + 341) return 0;
                    if (param === 7936 + 342) return 0;
                    if (param === 7936 + 343) return 0;
                    if (param === 7936 + 344) return 0;
                    if (param === 7936 + 345) return 0;
                    if (param === 7936 + 346) return 0;
                    if (param === 7936 + 347) return 0;
                    if (param === 7936 + 348) return 0;
                    if (param === 7936 + 349) return 0;
                    if (param === 7936 + 350) return 0;
                    if (param === 7936 + 351) return 0;
                    if (param === 7936 + 352) return 0;
                    if (param === 7936 + 353) return 0;
                    if (param === 7936 + 354) return 0;
                    if (param === 7936 + 355) return 0;
                    if (param === 7936 + 356) return 0;
                    if (param === 7936 + 357) return 0;
                    if (param === 7936 + 358) return 0;
                    if (param === 7936 + 359) return 0;
                    if (param === 7936 + 360) return 0;
                    if (param === 7936 + 361) return 0;
                    if (param === 7936 + 362) return 0;
                    if (param === 7936 + 363) return 0;
                    if (param === 7936 + 364) return 0;
                    if (param === 7936 + 365) return 0;
                    if (param === 7936 + 366) return 0;
                    if (param === 7936 + 367) return 0;
                    if (param === 7936 + 368) return 0;
                    if (param === 7936 + 369) return 0;
                    if (param === 7936 + 370) return 0;
                    if (param === 7936 + 371) return 0;
                    if (param === 7936 + 372) return 0;
                    if (param === 7936 + 373) return 0;
                    if (param === 7936 + 374) return 0;
                    if (param === 7936 + 375) return 0;
                    if (param === 7936 + 376) return 0;
                    if (param === 7936 + 377) return 0;
                    if (param === 7936 + 378) return 0;
                    if (param === 7936 + 379) return 0;
                    if (param === 7936 + 380) return 0;
                    if (param === 7936 + 381) return 0;
                    if (param === 7936 + 382) return 0;
                    if (param === 7936 + 383) return 0;
                    if (param === 7936 + 384) return 0;
                    if (param === 7936 + 385) return 0;
                    if (param === 7936 + 386) return 0;
                    if (param === 7936 + 387) return 0;
                    if (param === 7936 + 388) return 0;
                    if (param === 7936 + 389) return 0;
                    if (param === 7936 + 390) return 0;
                    if (param === 7936 + 391) return 0;
                    if (param === 7936 + 392) return 0;
                    if (param === 7936 + 393) return 0;
                    if (param === 7936 + 394) return 0;
                    if (param === 7936 + 395) return 0;
                    if (param === 7936 + 396) return 0;
                    if (param === 7936 + 397) return 0;
                    if (param === 7936 + 398) return 0;
                    if (param === 7936 + 399) return 0;
                    if (param === 7936 + 400) return 0;
                    if (param === 7936 + 401) return 0;
                    if (param === 7936 + 402) return 0;
                    if (param === 7936 + 403) return 0;
                    if (param === 7936 + 404) return 0;
                    if (param === 7936 + 405) return 0;
                    if (param === 7936 + 406) return 0;
                    if (param === 7936 + 407) return 0;
                    if (param === 7936 + 408) return 0;
                    if (param === 7936 + 409) return 0;
                    if (param === 7936 + 410) return 0;
                    if (param === 7936 + 411) return 0;
                    if (param === 7936 + 412) return 0;
                    if (param === 7936 + 413) return 0;
                    if (param === 7936 + 414) return 0;
                    if (param === 7936 + 415) return 0;
                    if (param === 7936 + 416) return 0;
                    if (param === 7936 + 417) return 0;
                    if (param === 7936 + 418) return 0;
                    if (param === 7936 + 419) return 0;
                    if (param === 7936 + 420) return 0;
                    if (param === 7936 + 421) return 0;
                    if (param === 7936 + 422) return 0;
                    if (param === 7936 + 423) return 0;
                    if (param === 7936 + 424) return 0;
                    if (param === 7936 + 425) return 0;
                    if (param === 7936 + 426) return 0;
                    if (param === 7936 + 427) return 0;
                    if (param === 7936 + 428) return 0;
                    if (param === 7936 + 429) return 0;
                    if (param === 7936 + 430) return 0;
                    if (param === 7936 + 431) return 0;
                    if (param === 7936 + 432) return 0;
                    if (param === 7936 + 433) return 0;
                    if (param === 7936 + 434) return 0;
                    if (param === 7936 + 435) return 0;
                    if (param === 7936 + 436) return 0;
                    if (param === 7936 + 437) return 0;
                    if (param === 7936 + 438) return 0;
                    if (param === 7936 + 439) return 0;
                    if (param === 7936 + 440) return 0;
                    if (param === 7936 + 441) return 0;
                    if (param === 7936 + 442) return 0;
                    if (param === 7936 + 443) return 0;
                    if (param === 7936 + 444) return 0;
                    if (param === 7936 + 445) return 0;
                    if (param === 7936 + 446) return 0;
                    if (param === 7936 + 447) return 0;
                    if (param === 7936 + 448) return 0;
                    if (param === 7936 + 449) return 0;
                    if (param === 7936 + 450) return 0;
                    if (param === 7936 + 451) return 0;
                    if (param === 7936 + 452) return 0;
                    if (param === 7936 + 453) return 0;
                    if (param === 7936 + 454) return 0;
                    if (param === 7936 + 455) return 0;
                    if (param === 7936 + 456) return 0;
                    if (param === 7936 + 457) return 0;
                    if (param === 7936 + 458) return 0;
                    if (param === 7936 + 459) return 0;
                    if (param === 7936 + 460) return 0;
                    if (param === 7936 + 461) return 0;
                    if (param === 7936 + 462) return 0;
                    if (param === 7936 + 463) return 0;
                    if (param === 7936 + 464) return 0;
                    if (param === 7936 + 465) return 0;
                    if (param === 7936 + 466) return 0;
                    if (param === 7936 + 467) return 0;
                    if (param === 7936 + 468) return 0;
                    if (param === 7936 + 469) return 0;
                    if (param === 7936 + 470) return 0;
                    if (param === 7936 + 471) return 0;
                    if (param === 7936 + 472) return 0;
                    if (param === 7936 + 473) return 0;
                    if (param === 7936 + 474) return 0;
                    if (param === 7936 + 475) return 0;
                    if (param === 7936 + 476) return 0;
                    if (param === 7936 + 477) return 0;
                    if (param === 7936 + 478) return 0;
                    if (param === 7936 + 479) return 0;
                    if (param === 7936 + 480) return 0;
                    if (param === 7936 + 481) return 0;
                    if (param === 7936 + 482) return 0;
                    if (param === 7936 + 483) return 0;
                    if (param === 7936 + 484) return 0;
                    if (param === 7936 + 485) return 0;
                    if (param === 7936 + 486) return 0;
                    if (param === 7936 + 487) return 0;
                    if (param === 7936 + 488) return 0;
                    if (param === 7936 + 489) return 0;
                    if (param === 7936 + 490) return 0;
                    if (param === 7936 + 491) return 0;
                    if (param === 7936 + 492) return 0;
                    if (param === 7936 + 493) return 0;
                    if (param === 7936 + 494) return 0;
                    if (param === 7936 + 495) return 0;
                    if (param === 7936 + 496) return 0;
                    if (param === 7936 + 497) return 0;
                    if (param === 7936 + 498) return 0;
                    if (param === 7936 + 499) return 0;
                    if (param === 7936 + 500) return 0;
                    if (param === 7936 + 501) return 0;
                    if (param === 7936 + 502) return 0;
                    if (param === 7936 + 503) return 0;
                    if (param === 7936 + 504) return 0;
                    if (param === 7936 + 505) return 0;
                    if (param === 7936 + 506) return 0;
                    if (param === 7936 + 507) return 0;
                    if (param === 7936 + 508) return 0;
                    if (param === 7936 + 509) return 0;
                    if (param === 7936 + 510) return 0;
                    if (param === 7936 + 511) return 0;
                    return originalGetParameter.call(this, param);
                };
                return ctx;
            } catch (e) {
                return dummyContext;
            }
        }
        return origGetContext.call(this, contextType, contextAttributes);
    };
    """

    has_webgl2 = """
    const dummyContext2 = {};
    const origGetContext2 = HTMLCanvasElement.prototype.getContext;
    HTMLCanvasElement.prototype.getContext = function(contextType, contextAttributes) {
        if (contextType === 'webgl2') {
            try {
                const ctx2 = origGetContext2.call(this, 'webgl2', contextAttributes);
                if (!ctx2) return dummyContext2;
                const origGetParameter2 = ctx2.getParameter.bind(ctx2);
                ctx2.getParameter = function(param) {
                    if (param === 37445) return 'Intel Inc.';
                    if (param === 37446) return 'Intel Iris OpenGL Engine';
                    if (param === 3412) return 0;
                    if (param === 3413) return 0;
                    if (param === 3414) return 1;
                    if (param === 3415) return 8;
                    if (param === 7936) return 'Intel Iris OpenGL Engine';
                    if (param === 7937) return 'Intel Iris OpenGL Engine';
                    if (param === 7938) return 255;
                    if (param === 7939) return 218762004;
                    if (param === 7940) return 942810852;
                    if (param === 7941) return 897589952;
                    if (param === 7944) return 131072;
                    if (param === 7945) return 0;
                    if (param === 7936 + 1) return 1;
                    if (param === 7936 + 2) return 24;
                    if (param === 7936 + 3) return 8;
                    if (param === 7936 + 4) return 24;
                    if (param === 7936 + 5) return 8;
                    if (param === 7936 + 6) return 0;
                    if (param === 7936 + 7) return 0;
                    if (param === 7936 + 8) return 0;
                    if (param === 7936 + 9) return 0;
                    if (param === 7936 + 10) return 0;
                    if (param === 7936 + 11) return 0;
                    if (param === 7936 + 12) return 0;
                    if (param === 7936 + 13) return 0;
                    if (param === 7936 + 14) return 0;
                    if (param === 7936 + 15) return 0;
                    if (param === 7936 + 16) return 1;
                    if (param === 7936 + 17) return 16384;
                    if (param === 7936 + 18) return 0;
                    if (param === 7936 + 19) return 16384;
                    if (param === 7936 + 20) return 0;
                    if (param === 7936 + 21) return 4;
                    if (param === 7936 + 22) return 0;
                    if (param === 7936 + 23) return 0;
                    if (param === 7936 + 24) return 0;
                    if (param === 7936 + 25) return 0;
                    if (param === 7936 + 26) return 1;
                    if (param === 7936 + 27) return 0;
                    if (param === 7936 + 28) return 0;
                    if (param === 7936 + 29) return 16384;
                    if (param === 7936 + 30) return 0;
                    if (param === 7936 + 31) return 0;
                    if (param === 7936 + 32) return 0;
                    if (param === 7936 + 33) return 0;
                    if (param === 7936 + 34) return 0;
                    if (param === 7936 + 35) return 0;
                    if (param === 7936 + 36) return 0;
                    if (param === 7936 + 37) return 1;
                    if (param === 7936 + 38) return 0;
                    if (param === 7936 + 39) return 1;
                    if (param === 7936 + 40) return 0;
                    if (param === 7936 + 41) return 0;
                    if (param === 7936 + 42) return 0;
                    if (param === 7936 + 43) return 0;
                    if (param === 7936 + 44) return 0;
                    if (param === 7936 + 45) return 0;
                    if (param === 7936 + 46) return 0;
                    if (param === 7936 + 47) return 0;
                    if (param === 7936 + 48) return 0;
                    if (param === 7936 + 49) return 0;
                    if (param === 7936 + 50) return 0;
                    if (param === 7936 + 51) return 0;
                    if (param === 7936 + 52) return 0;
                    if (param === 7936 + 53) return 1;
                    if (param === 7936 + 54) return 1;
                    if (param === 7936 + 55) return 1;
                    if (param === 7936 + 56) return 0;
                    if (param === 7936 + 57) return 0;
                    if (param === 7936 + 58) return 0;
                    if (param === 7936 + 59) return 0;
                    if (param === 7936 + 60) return 0;
                    if (param === 7936 + 61) return 0;
                    if (param === 7936 + 62) return 0;
                    if (param === 7936 + 63) return 0;
                    if (param === 7936 + 64) return 0;
                    if (param === 7936 + 65) return 0;
                    if (param === 7936 + 66) return 0;
                    if (param === 7936 + 67) return 0;
                    if (param === 7936 + 68) return 0;
                    if (param === 7936 + 69) return 0;
                    if (param === 7936 + 70) return 0;
                    if (param === 7936 + 71) return 0;
                    if (param === 7936 + 72) return 0;
                    if (param === 7936 + 73) return 0;
                    if (param === 7936 + 74) return 0;
                    if (param === 7936 + 75) return 0;
                    if (param === 7936 + 76) return 0;
                    if (param === 7936 + 77) return 1;
                    if (param === 7936 + 78) return 0;
                    if (param === 7936 + 79) return 0;
                    if (param === 7936 + 80) return 1;
                    if (param === 7936 + 81) return 0;
                    if (param === 7936 + 82) return 0;
                    if (param === 7936 + 83) return 0;
                    if (param === 7936 + 84) return 0;
                    if (param === 7936 + 85) return 0;
                    if (param === 7936 + 86) return 0;
                    if (param === 7936 + 87) return 0;
                    if (param === 7936 + 88) return 0;
                    if (param === 7936 + 89) return 0;
                    if (param === 7936 + 90) return 0;
                    if (param === 7936 + 91) return 0;
                    if (param === 7936 + 92) return 0;
                    if (param === 7936 + 93) return 0;
                    if (param === 7936 + 94) return 0;
                    if (param === 7936 + 95) return 0;
                    if (param === 7936 + 96) return 0;
                    if (param === 7936 + 97) return 0;
                    if (param === 7936 + 98) return 0;
                    if (param === 7936 + 99) return 0;
                    if (param === 7936 + 100) return 0;
                    if (param === 7936 + 101) return 0;
                    if (param === 7936 + 102) return 0;
                    if (param === 7936 + 103) return 0;
                    if (param === 7936 + 104) return 0;
                    if (param === 7936 + 105) return 0;
                    if (param === 7936 + 106) return 0;
                    if (param === 7936 + 107) return 0;
                    if (param === 7936 + 108) return 0;
                    if (param === 7936 + 109) return 0;
                    if (param === 7936 + 110) return 0;
                    if (param === 7936 + 111) return 0;
                    if (param === 7936 + 112) return 0;
                    if (param === 7936 + 113) return 0;
                    if (param === 7936 + 114) return 0;
                    if (param === 7936 + 115) return 0;
                    if (param === 7936 + 116) return 0;
                    if (param === 7936 + 117) return 0;
                    if (param === 7936 + 118) return 0;
                    if (param === 7936 + 119) return 0;
                    if (param === 7936 + 120) return 0;
                    if (param === 7936 + 121) return 0;
                    if (param === 7936 + 122) return 0;
                    if (param === 7936 + 123) return 0;
                    if (param === 7936 + 124) return 0;
                    if (param === 7936 + 125) return 0;
                    if (param === 7936 + 126) return 0;
                    if (param === 7936 + 127) return 0;
                    if (param === 7936 + 128) return 0;
                    if (param === 7936 + 129) return 0;
                    if (param === 7936 + 130) return 0;
                    if (param === 7936 + 131) return 0;
                    if (param === 7936 + 132) return 0;
                    if (param === 7936 + 133) return 0;
                    if (param === 7936 + 134) return 0;
                    if (param === 7936 + 135) return 0;
                    if (param === 7936 + 136) return 0;
                    if (param === 7936 + 137) return 0;
                    if (param === 7936 + 138) return 0;
                    if (param === 7936 + 139) return 0;
                    if (param === 7936 + 140) return 0;
                    if (param === 7936 + 141) return 0;
                    if (param === 7936 + 142) return 0;
                    if (param === 7936 + 143) return 0;
                    if (param === 7936 + 144) return 0;
                    if (param === 7936 + 145) return 0;
                    if (param === 7936 + 146) return 0;
                    if (param === 7936 + 147) return 0;
                    if (param === 7936 + 148) return 0;
                    if (param === 7936 + 149) return 0;
                    if (param === 7936 + 150) return 0;
                    if (param === 7936 + 151) return 0;
                    if (param === 7936 + 152) return 0;
                    if (param === 7936 + 153) return 0;
                    if (param === 7936 + 154) return 0;
                    if (param === 7936 + 155) return 0;
                    if (param === 7936 + 156) return 0;
                    if (param === 7936 + 157) return 0;
                    if (param === 7936 + 158) return 0;
                    if (param === 7936 + 159) return 0;
                    if (param === 7936 + 160) return 0;
                    if (param === 7936 + 161) return 0;
                    if (param === 7936 + 162) return 0;
                    if (param === 7936 + 163) return 0;
                    if (param === 7936 + 164) return 0;
                    if (param === 7936 + 165) return 0;
                    if (param === 7936 + 166) return 0;
                    if (param === 7936 + 167) return 0;
                    if (param === 7936 + 168) return 0;
                    if (param === 7936 + 169) return 0;
                    if (param === 7936 + 170) return 0;
                    if (param === 7936 + 171) return 0;
                    if (param === 7936 + 172) return 0;
                    if (param === 7936 + 173) return 0;
                    if (param === 7936 + 174) return 0;
                    if (param === 7936 + 175) return 0;
                    if (param === 7936 + 176) return 0;
                    if (param === 7936 + 177) return 0;
                    if (param === 7936 + 178) return 0;
                    if (param === 7936 + 179) return 0;
                    if (param === 7936 + 180) return 0;
                    if (param === 7936 + 181) return 0;
                    if (param === 7936 + 182) return 0;
                    if (param === 7936 + 183) return 0;
                    if (param === 7936 + 184) return 0;
                    if (param === 7936 + 185) return 0;
                    if (param === 7936 + 186) return 0;
                    if (param === 7936 + 187) return 0;
                    if (param === 7936 + 188) return 0;
                    if (param === 7936 + 189) return 0;
                    if (param === 7936 + 190) return 0;
                    if (param === 7936 + 191) return 0;
                    if (param === 7936 + 192) return 0;
                    if (param === 7936 + 193) return 0;
                    if (param === 7936 + 194) return 0;
                    if (param === 7936 + 195) return 0;
                    if (param === 7936 + 196) return 0;
                    if (param === 7936 + 197) return 0;
                    if (param === 7936 + 198) return 0;
                    if (param === 7936 + 199) return 0;
                    if (param === 7936 + 200) return 0;
                    if (param === 7936 + 201) return 0;
                    if (param === 7936 + 202) return 0;
                    if (param === 7936 + 203) return 0;
                    if (param === 7936 + 204) return 0;
                    if (param === 7936 + 205) return 0;
                    if (param === 7936 + 206) return 0;
                    if (param === 7936 + 207) return 0;
                    if (param === 7936 + 208) return 0;
                    if (param === 7936 + 209) return 0;
                    if (param === 7936 + 210) return 0;
                    if (param === 7936 + 211) return 0;
                    if (param === 7936 + 212) return 0;
                    if (param === 7936 + 213) return 0;
                    if (param === 7936 + 214) return 0;
                    if (param === 7936 + 215) return 0;
                    if (param === 7936 + 216) return 0;
                    if (param === 7936 + 217) return 0;
                    if (param === 7936 + 218) return 0;
                    if (param === 7936 + 219) return 0;
                    if (param === 7936 + 220) return 0;
                    if (param === 7936 + 221) return 0;
                    if (param === 7936 + 222) return 0;
                    if (param === 7936 + 223) return 0;
                    if (param === 7936 + 224) return 0;
                    if (param === 7936 + 225) return 0;
                    if (param === 7936 + 226) return 0;
                    if (param === 7936 + 227) return 0;
                    if (param === 7936 + 228) return 0;
                    if (param === 7936 + 229) return 0;
                    if (param === 7936 + 230) return 0;
                    if (param === 7936 + 231) return 0;
                    if (param === 7936 + 232) return 0;
                    if (param === 7936 + 233) return 0;
                    if (param === 7936 + 234) return 0;
                    if (param === 7936 + 235) return 0;
                    if (param === 7936 + 236) return 0;
                    if (param === 7936 + 237) return 0;
                    if (param === 7936 + 238) return 0;
                    if (param === 7936 + 239) return 0;
                    if (param === 7936 + 240) return 0;
                    if (param === 7936 + 241) return 0;
                    if (param === 7936 + 242) return 0;
                    if (param === 7936 + 243) return 0;
                    if (param === 7936 + 244) return 0;
                    if (param === 7936 + 245) return 0;
                    if (param === 7936 + 246) return 0;
                    if (param === 7936 + 247) return 0;
                    if (param === 7936 + 248) return 0;
                    if (param === 7936 + 249) return 0;
                    if (param === 7936 + 250) return 0;
                    if (param === 7936 + 251) return 0;
                    if (param === 7936 + 252) return 0;
                    if (param === 7936 + 253) return 0;
                    if (param === 7936 + 254) return 0;
                    if (param === 7936 + 255) return 0;
                    if (param === 7936 + 256) return 0;
                    if (param === 7936 + 257) return 0;
                    if (param === 7936 + 258) return 0;
                    if (param === 7936 + 259) return 0;
                    if (param === 7936 + 260) return 0;
                    if (param === 7936 + 261) return 0;
                    if (param === 7936 + 262) return 0;
                    if (param === 7936 + 263) return 0;
                    if (param === 7936 + 264) return 0;
                    if (param === 7936 + 265) return 0;
                    if (param === 7936 + 266) return 0;
                    if (param === 7936 + 267) return 0;
                    if (param === 7936 + 268) return 0;
                    if (param === 7936 + 269) return 0;
                    if (param === 7936 + 270) return 0;
                    if (param === 7936 + 271) return 0;
                    if (param === 7936 + 272) return 0;
                    if (param === 7936 + 273) return 0;
                    if (param === 7936 + 274) return 0;
                    if (param === 7936 + 275) return 0;
                    if (param === 7936 + 276) return 0;
                    if (param === 7936 + 277) return 0;
                    if (param === 7936 + 278) return 0;
                    if (param === 7936 + 279) return 0;
                    if (param === 7936 + 280) return 0;
                    if (param === 7936 + 281) return 0;
                    if (param === 7936 + 282) return 0;
                    if (param === 7936 + 283) return 0;
                    if (param === 7936 + 284) return 0;
                    if (param === 7936 + 285) return 0;
                    if (param === 7936 + 286) return 0;
                    if (param === 7936 + 287) return 0;
                    if (param === 7936 + 288) return 0;
                    if (param === 7936 + 289) return 0;
                    if (param === 7936 + 290) return 0;
                    if (param === 7936 + 291) return 0;
                    if (param === 7936 + 292) return 0;
                    if (param === 7936 + 293) return 0;
                    if (param === 7936 + 294) return 0;
                    if (param === 7936 + 295) return 0;
                    if (param === 7936 + 296) return 0;
                    if (param === 7936 + 297) return 0;
                    if (param === 7936 + 298) return 0;
                    if (param === 7936 + 299) return 0;
                    if (param === 7936 + 300) return 0;
                    if (param === 7936 + 301) return 0;
                    if (param === 7936 + 302) return 0;
                    if (param === 7936 + 303) return 0;
                    if (param === 7936 + 304) return 0;
                    if (param === 7936 + 305) return 0;
                    if (param === 7936 + 306) return 0;
                    if (param === 7936 + 307) return 0;
                    if (param === 7936 + 308) return 0;
                    if (param === 7936 + 309) return 0;
                    if (param === 7936 + 310) return 0;
                    if (param === 7936 + 311) return 0;
                    if (param === 7936 + 312) return 0;
                    if (param === 7936 + 313) return 0;
                    if (param === 7936 + 314) return 0;
                    if (param === 7936 + 315) return 0;
                    if (param === 7936 + 316) return 0;
                    if (param === 7936 + 317) return 0;
                    if (param === 7936 + 318) return 0;
                    if (param === 7936 + 319) return 0;
                    if (param === 7936 + 320) return 0;
                    if (param === 7936 + 321) return 0;
                    if (param === 7936 + 322) return 0;
                    if (param === 7936 + 323) return 0;
                    if (param === 7936 + 324) return 0;
                    if (param === 7936 + 325) return 0;
                    if (param === 7936 + 326) return 0;
                    if (param === 7936 + 327) return 0;
                    if (param === 7936 + 328) return 0;
                    if (param === 7936 + 329) return 0;
                    if (param === 7936 + 330) return 0;
                    if (param === 7936 + 331) return 0;
                    if (param === 7936 + 332) return 0;
                    if (param === 7936 + 333) return 0;
                    if (param === 7936 + 334) return 0;
                    if (param === 7936 + 335) return 0;
                    if (param === 7936 + 336) return 0;
                    if (param === 7936 + 337) return 0;
                    if (param === 7936 + 338) return 0;
                    if (param === 7936 + 339) return 0;
                    if (param === 7936 + 340) return 0;
                    if (param === 7936 + 341) return 0;
                    if (param === 7936 + 342) return 0;
                    if (param === 7936 + 343) return 0;
                    if (param === 7936 + 344) return 0;
                    if (param === 7936 + 345) return 0;
                    if (param === 7936 + 346) return 0;
                    if (param === 7936 + 347) return 0;
                    if (param === 7936 + 348) return 0;
                    if (param === 7936 + 349) return 0;
                    if (param === 7936 + 350) return 0;
                    if (param === 7936 + 351) return 0;
                    if (param === 7936 + 352) return 0;
                    if (param === 7936 + 353) return 0;
                    if (param === 7936 + 354) return 0;
                    if (param === 7936 + 355) return 0;
                    if (param === 7936 + 356) return 0;
                    if (param === 7936 + 357) return 0;
                    if (param === 7936 + 358) return 0;
                    if (param === 7936 + 359) return 0;
                    if (param === 7936 + 360) return 0;
                    if (param === 7936 + 361) return 0;
                    if (param === 7936 + 362) return 0;
                    if (param === 7936 + 363) return 0;
                    if (param === 7936 + 364) return 0;
                    if (param === 7936 + 365) return 0;
                    if (param === 7936 + 366) return 0;
                    if (param === 7936 + 367) return 0;
                    if (param === 7936 + 368) return 0;
                    if (param === 7936 + 369) return 0;
                    if (param === 7936 + 370) return 0;
                    if (param === 7936 + 371) return 0;
                    if (param === 7936 + 372) return 0;
                    if (param === 7936 + 373) return 0;
                    if (param === 7936 + 374) return 0;
                    if (param === 7936 + 375) return 0;
                    if (param === 7936 + 376) return 0;
                    if (param === 7936 + 377) return 0;
                    if (param === 7936 + 378) return 0;
                    if (param === 7936 + 379) return 0;
                    if (param === 7936 + 380) return 0;
                    if (param === 7936 + 381) return 0;
                    if (param === 7936 + 382) return 0;
                    if (param === 7936 + 383) return 0;
                    if (param === 7936 + 384) return 0;
                    if (param === 7936 + 385) return 0;
                    if (param === 7936 + 386) return 0;
                    if (param === 7936 + 387) return 0;
                    if (param === 7936 + 388) return 0;
                    if (param === 7936 + 389) return 0;
                    if (param === 7936 + 390) return 0;
                    if (param === 7936 + 391) return 0;
                    if (param === 7936 + 392) return 0;
                    if (param === 7936 + 393) return 0;
                    if (param === 7936 + 394) return 0;
                    if (param === 7936 + 395) return 0;
                    if (param === 7936 + 396) return 0;
                    if (param === 7936 + 397) return 0;
                    if (param === 7936 + 398) return 0;
                    if (param === 7936 + 399) return 0;
                    if (param === 7936 + 400) return 0;
                    if (param === 7936 + 401) return 0;
                    if (param === 7936 + 402) return 0;
                    if (param === 7936 + 403) return 0;
                    if (param === 7936 + 404) return 0;
                    if (param === 7936 + 405) return 0;
                    if (param === 7936 + 406) return 0;
                    if (param === 7936 + 407) return 0;
                    if (param === 7936 + 408) return 0;
                    if (param === 7936 + 409) return 0;
                    if (param === 7936 + 410) return 0;
                    if (param === 7936 + 411) return 0;
                    if (param === 7936 + 412) return 0;
                    if (param === 7936 + 413) return 0;
                    if (param === 7936 + 414) return 0;
                    if (param === 7936 + 415) return 0;
                    if (param === 7936 + 416) return 0;
                    if (param === 7936 + 417) return 0;
                    if (param === 7936 + 418) return 0;
                    if (param === 7936 + 419) return 0;
                    if (param === 7936 + 420) return 0;
                    if (param === 7936 + 421) return 0;
                    if (param === 7936 + 422) return 0;
                    if (param === 7936 + 423) return 0;
                    if (param === 7936 + 424) return 0;
                    if (param === 7936 + 425) return 0;
                    if (param === 7936 + 426) return 0;
                    if (param === 7936 + 427) return 0;
                    if (param === 7936 + 428) return 0;
                    if (param === 7936 + 429) return 0;
                    if (param === 7936 + 430) return 0;
                    if (param === 7936 + 431) return 0;
                    if (param === 7936 + 432) return 0;
                    if (param === 7936 + 433) return 0;
                    if (param === 7936 + 434) return 0;
                    if (param === 7936 + 435) return 0;
                    if (param === 7936 + 436) return 0;
                    if (param === 7936 + 437) return 0;
                    if (param === 7936 + 438) return 0;
                    if (param === 7936 + 439) return 0;
                    if (param === 7936 + 440) return 0;
                    if (param === 7936 + 441) return 0;
                    if (param === 7936 + 442) return 0;
                    if (param === 7936 + 443) return 0;
                    if (param === 7936 + 444) return 0;
                    if (param === 7936 + 445) return 0;
                    if (param === 7936 + 446) return 0;
                    if (param === 7936 + 447) return 0;
                    if (param === 7936 + 448) return 0;
                    if (param === 7936 + 449) return 0;
                    if (param === 7936 + 450) return 0;
                    if (param === 7936 + 451) return 0;
                    if (param === 7936 + 452) return 0;
                    if (param === 7936 + 453) return 0;
                    if (param === 7936 + 454) return 0;
                    if (param === 7936 + 455) return 0;
                    if (param === 7936 + 456) return 0;
                    if (param === 7936 + 457) return 0;
                    if (param === 7936 + 458) return 0;
                    if (param === 7936 + 459) return 0;
                    if (param === 7936 + 460) return 0;
                    if (param === 7936 + 461) return 0;
                    if (param === 7936 + 462) return 0;
                    if (param === 7936 + 463) return 0;
                    if (param === 7936 + 464) return 0;
                    if (param === 7936 + 465) return 0;
                    if (param === 7936 + 466) return 0;
                    if (param === 7936 + 467) return 0;
                    if (param === 7936 + 468) return 0;
                    if (param === 7936 + 469) return 0;
                    if (param === 7936 + 470) return 0;
                    if (param === 7936 + 471) return 0;
                    if (param === 7936 + 472) return 0;
                    if (param === 7936 + 473) return 0;
                    if (param === 7936 + 474) return 0;
                    if (param === 7936 + 475) return 0;
                    if (param === 7936 + 476) return 0;
                    if (param === 7936 + 477) return 0;
                    if (param === 7936 + 478) return 0;
                    if (param === 7936 + 479) return 0;
                    if (param === 7936 + 480) return 0;
                    if (param === 7936 + 481) return 0;
                    if (param === 7936 + 482) return 0;
                    if (param === 7936 + 483) return 0;
                    if (param === 7936 + 484) return 0;
                    if (param === 7936 + 485) return 0;
                    if (param === 7936 + 486) return 0;
                    if (param === 7936 + 487) return 0;
                    if (param === 7936 + 488) return 0;
                    if (param === 7936 + 489) return 0;
                    if (param === 7936 + 490) return 0;
                    if (param === 7936 + 491) return 0;
                    if (param === 7936 + 492) return 0;
                    if (param === 7936 + 493) return 0;
                    if (param === 7936 + 494) return 0;
                    if (param === 7936 + 495) return 0;
                    if (param === 7936 + 496) return 0;
                    if (param === 7936 + 497) return 0;
                    if (param === 7936 + 498) return 0;
                    if (param === 7936 + 499) return 0;
                    if (param === 7936 + 500) return 0;
                    if (param === 7936 + 501) return 0;
                    if (param === 7936 + 502) return 0;
                    if (param === 7936 + 503) return 0;
                    if (param === 7936 + 504) return 0;
                    if (param === 7936 + 505) return 0;
                    if (param === 7936 + 506) return 0;
                    if (param === 7936 + 507) return 0;
                    if (param === 7936 + 508) return 0;
                    if (param === 7936 + 509) return 0;
                    if (param === 7936 + 510) return 0;
                    if (param === 7936 + 511) return 0;
                    return origGetParameter2(param);
                };
                return ctx2;
            } catch (e) {
                return dummyContext2;
            }
        }
        return origGetContext2.call(this, contextType, contextAttributes);
    };
    """

    has_canvas = """
    const origToDataURL = HTMLCanvasElement.prototype.toDataURL;
    const origToBlob = HTMLCanvasElement.prototype.toBlob;
    const origGetImageData = CanvasRenderingContext2D.prototype.getImageData;
    let _canvasNoise = null;
    function _addCanvasNoise(context) {
        if (_canvasNoise !== null) return;
        try {
            const width = context.canvas.width;
            const height = context.canvas.height;
            if (width === 0 || height === 0) return;
            const imageData = context.getImageData(0, 0, width, height);
            const data = imageData.data;
            for (let i = 0; i < data.length; i += 4) {
                const noise = (Math.random() - 0.5) * 0.4;
                data[i] = Math.min(255, Math.max(0, data[i] + noise));
                data[i+1] = Math.min(255, Math.max(0, data[i+1] + noise));
                data[i+2] = Math.min(255, Math.max(0, data[i+2] + noise));
            }
            context.putImageData(imageData, 0, 0);
        } catch(e) {}
    }
    HTMLCanvasElement.prototype.toDataURL = function() {
        try { _addCanvasNoise(this.getContext('2d')); } catch(e) {}
        return origToDataURL.apply(this, arguments);
    };
    HTMLCanvasElement.prototype.toBlob = function() {
        try { _addCanvasNoise(this.getContext('2d')); } catch(e) {}
        return origToBlob.apply(this, arguments);
    };
    CanvasRenderingContext2D.prototype.getImageData = function() {
        try { _addCanvasNoise(this); } catch(e) {}
        return origGetImageData.apply(this, arguments);
    };
    """

    has_webgl_params = """
    const origGetExtension = WebGLRenderingContext.prototype.getExtension;
    const origGetParameter = WebGLRenderingContext.prototype.getParameter;
    const origGetShaderPrecisionFormat = WebGLRenderingContext.prototype.getShaderPrecisionFormat;
    const UNMASKED_VENDOR_WEBGL = 0x9245;
    const UNMASKED_RENDERER_WEBGL = 0x9246;
    WebGLRenderingContext.prototype.getExtension = function(name) {
        try {
            const ext = origGetExtension.call(this, name);
            return ext;
        } catch (e) { return null; }
    };
    WebGLRenderingContext.prototype.getParameter = function(param) {
        if (param === UNMASKED_VENDOR_WEBGL) return 'Intel Inc.';
        if (param === UNMASKED_RENDERER_WEBGL) return 'Intel Iris OpenGL Engine';
        try {
            return origGetParameter.call(this, param);
        } catch (e) { return 0; }
    };
    WebGLRenderingContext.prototype.getShaderPrecisionFormat = function() {
        try {
            return origGetShaderPrecisionFormat.apply(this, arguments);
        } catch (e) {
            return {rangeMin: 1, rangeMax: 1, precision: 1};
        }
    };
    """

    has_chrome_runtime = """
    window.chrome = (function() {
        function Chrome() {}
        Chrome.prototype.runtime = (function() {
            function Runtime() {}
            Runtime.prototype.connect = function() { return {}; };
            Runtime.prototype.sendMessage = function() { return {}; };
            Runtime.prototype.id = Math.random().toString(36).substring(7);
            Runtime.prototype.LAST_ERROR = undefined;
            Runtime.prototype.onConnect = { addListener: function() {} };
            Runtime.prototype.onMessage = { addListener: function() {} };
            Runtime.prototype.getManifest = function() {
                return {"manifest_version": 3, "name": "Chrome", "version": "126.0.0.0"};
            };
            return new Runtime();
        })();
        Chrome.prototype.loadTimes = function() { return {}; };
        Chrome.prototype.csi = function() { return {}; };
        Chrome.prototype.app = {};
        Chrome.prototype.webstore = {};
        Chrome.prototype.storage = {
            sync: { get: function() {}, set: function() {}, remove: function() {} },
            local: { get: function() {}, set: function() {}, remove: function() {} }
        };
        return new Chrome();
    })();
    Object.defineProperty(window, 'chrome', {
        writable: true,
        configurable: false,
        enumerable: true,
        value: window.chrome
    });
    """

    has_plugins = """
    const _plugins = [
        { name: 'Chrome PDF Plugin', description: 'Portable Document Format', suffixes: 'pdf', enabledPlugin: true, filename: 'internal-pdf-viewer' },
        { name: 'Chrome PDF Viewer', description: '', suffixes: 'pdf', enabledPlugin: false, filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' },
        { name: 'Native Client', description: '', suffixes: '', enabledPlugin: false, filename: 'internal-nacl' }
    ];
    Object.defineProperty(navigator, 'plugins', {
        get: function() { return _plugins; },
        configurable: true,
        enumerable: true
    });
    Object.defineProperty(navigator, 'mimeTypes', {
        get: function() {
            return [
                { type: 'application/pdf', description: 'Portable Document Format', suffixes: 'pdf', enabledPlugin: true },
                { type: 'application/x-nacl', description: 'Native Client Executable', suffixes: 'nexe', enabledPlugin: true },
                { type: 'application/x-pnacl', description: 'Portable Native Client Executable', suffixes: 'pnxe', enabledPlugin: true }
            ];
        },
        configurable: true,
        enumerable: true
    });
    """

    has_permissions = """
    const _permissions = ['geolocation', 'notifications', 'push', 'microphone', 'camera', 'speaker', 'device-info', 'bluetooth', 'serial', 'usb', 'hid', 'fido-authenticator'];
    const _cachedPermissions = {};
    Object.defineProperty(navigator, 'permissions', {
        get: function() {
            const self = this;
            return {
                query: function(permissionDesc) {
                    return Promise.resolve({
                        state: _cachedPermissions[permissionDesc.name] || 'prompt',
                        onchange: null,
                        addEventListener: function() {},
                        removeEventListener: function() {},
                        dispatchEvent: function() { return true; }
                    });
                },
                revoke: function(permissionDesc) {
                    return Promise.resolve({ state: 'prompt' });
                }
            };
        },
        configurable: true,
        enumerable: true
    });
    """

    has_language = """
    Object.defineProperty(navigator, 'languages', {
        get: function() { return ['zh-CN', 'zh', 'zh-TW', 'en-US', 'en']; },
        configurable: true,
        enumerable: true
    });
    Object.defineProperty(navigator, 'language', {
        get: function() { return 'zh-CN'; },
        configurable: true,
        enumerable: true
    });
    Object.defineProperty(navigator, 'langauge', {
        get: function() { return 'zh-CN'; },
        configurable: true,
        enumerable: true
    });
    """

    has_proxy = """
    Object.defineProperty(navigator, 'proxy', {
        get: function() { return {}; },
        configurable: true,
        enumerable: true
    });
    """

    has_dnt = """
    Object.defineProperty(navigator, 'doNotTrack', {
        get: function() { return '1'; },
        configurable: true,
        enumerable: true
    });
    """

    has_platform = """
    Object.defineProperty(navigator, 'platform', {
        get: function() { return 'Win32'; },
        configurable: true,
        enumerable: true
    });
    Object.defineProperty(navigator, 'oscpu', {
        get: function() { return 'Windows NT 10.0'; },
        configurable: true,
        enumerable: true
    });
    """

    has_hardware_concurrency = """
    Object.defineProperty(navigator, 'hardwareConcurrency', {
        get: function() { return 8; },
        configurable: true,
        enumerable: true
    });
    """

    has_device_memory = """
    Object.defineProperty(navigator, 'deviceMemory', {
        get: function() { return 8; },
        configurable: true,
        enumerable: true
    });
    """

    has_screen_size = """
    Object.defineProperty(screen, 'width', { get: function() { return 1920; }, configurable: true, enumerable: true });
    Object.defineProperty(screen, 'height', { get: function() { return 1080; }, configurable: true, enumerable: true });
    Object.defineProperty(screen, 'availWidth', { get: function() { return 1920; }, configurable: true, enumerable: true });
    Object.defineProperty(screen, 'availHeight', { get: function() { return 1040; }, configurable: true, enumerable: true });
    Object.defineProperty(screen, 'colorDepth', { get: function() { return 24; }, configurable: true, enumerable: true });
    Object.defineProperty(screen, 'pixelDepth', { get: function() { return 24; }, configurable: true, enumerable: true });
    """

    has_pdf = """
    Object.defineProperty(HTMLElement.prototype, '特性', {
        get: function() { return 'attributs'; },
        configurable: true,
        enumerable: true
    });
    """

    has_history = """
    Object.defineProperty(history, 'length', {
        get: function() { return randomInt(1, 10) + 1; },
        configurable: true,
        enumerable: true
    });
    function randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    """

    has_media = """
    Object.defineProperty(HTMLMediaElement.prototype, 'controlles', {
        get: function() { return false; },
        configurable: true,
        enumerable: true
    });
    Object.defineProperty(HTMLMediaElement.prototype, 'controls', {
        get: function() { return true; },
        configurable: true,
        enumerable: true
    });
    """

    has_webgl_vendor = """
    const origGetExtension = WebGLRenderingContext.prototype.getExtension;
    WebGLRenderingContext.prototype.getExtension = function(name) {
        if (name === 'WEBGL_debug_renderer_info') {
            return {
                UNMASKED_VENDOR_WEBGL: 0x9245,
                UNMASKED_RENDERER_WEBGL: 0x9246
            };
        }
        try {
            return origGetExtension.call(this, name);
        } catch (e) {
            return null;
        }
    };
    """

    scripts = []
    scripts.append(has_navigator_webdriver)
    if fix_webgl:
        scripts.append(has_webgl)
    if fix_webgl2:
        scripts.append(has_webgl2)
    if fix_canvas:
        scripts.append(has_canvas)
    if fix_webgl_params:
        scripts.append(has_webgl_params)
    if fix_clr:
        scripts.append(has_chrome_runtime)
    if fix_chrome:
        scripts.append(has_plugins)
    if fix_permissions:
        scripts.append(has_permissions)
    if fix_language:
        scripts.append(has_language)
    if fix_proxy:
        scripts.append(has_proxy)
    if fix_dnt:
        scripts.append(has_dnt)
    if fix_platform:
        scripts.append(has_platform)
    if fix_hardware_concurrency:
        scripts.append(has_hardware_concurrency)
    if fix_device_memory:
        scripts.append(has_device_memory)
    if fix_screen_size:
        scripts.append(has_screen_size)
    if fix_pdf:
        scripts.append(has_pdf)
    if fix_history:
        scripts.append(has_history)
    if fix_media:
        scripts.append(has_media)
    if fix_geolocation:
        scripts.append("""
        navigator.geolocation.getCurrentPosition = function(success, error, options) {
            success({ coords: { latitude: 39.9042, longitude: 116.4074, accuracy: 100, altitude: null, altitudeAccuracy: null, heading: null, speed: null }, timestamp: Date.now() });
        };
        navigator.geolocation.watchPosition = function(success, error, options) {
            success({ coords: { latitude: 39.9042, longitude: 116.4074, accuracy: 100, altitude: null, altitudeAccuracy: null, heading: null, speed: null }, timestamp: Date.now() });
        };
        Object.defineProperty(navigator, 'geolocation', {
            get: function() { return {
                getCurrentPosition: function(success) { success({ coords: { latitude: 39.9042, longitude: 116.4074 } }); },
                watchPosition: function(success) { success({ coords: { latitude: 39.9042, longitude: 116.4074 } }); }
            }; },
            configurable: true,
            enumerable: true
        });
        """)

    full_source = ";".join(scripts)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": full_source})


def apply_stealth(driver: webdriver.Chrome) -> None:
    try:
        base_stealth(
            driver,
            languages=["zh-CN", "zh", "en"],
            vendor="Google",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
    except Exception:
        pass

    try:
        _stealth_chrome(driver)
    except Exception:
        pass

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        delete window.webdriver;
        delete navigator.webdriver;
        try {
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        } catch(e) {}
        """
    })


def build_stealth_chrome(config: AppConfig) -> webdriver.Chrome:
    options = Options()
    options.add_argument(f"--window-size={config.window_size}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--remote-debugging-port=9222")

    prefs: dict[str, Any] = {
        "profile.default_content_setting_values.notifications": 1,
        "profile.default_content_settings.popups": 0,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_valuesnotifications": 1,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", [
        "enable-automation",
        "enable-logging",
        "disable-background-networking",
        "disable-client-side-phishing-detection",
        "disable-default-apps",
        "disable-hang-monitor",
        "disable-infobars",
        "disable-logging",
        "disable-log-redirect",
        "disable-optimize-benefits",
        "disable-password-reauthentication",
        "disable-promotional-popups",
        "disable-save-password-bubble",
        "disable-search-engine-ranked-choice",
        "disable-signin-promo-link-capturing",
        "disable-speech-input",
        "disable-sync",
        "disable-sync-settings",
        "disable-tab-for-desktop-share",
        "disable-voice-input",
        "disable-wake-on-wifi",
        "enable-async-dns",
        "enable-background-tabs",
        "enable-feature-policy",
        "enable-logging",
        "enable-network-information",
        "enable-predidential-processing",
        "enable-quick-answers",
        "enable-site-settings",
        "enable-strict-mode",
        "enable-web-contents",
        "enable-zero-copy",
        "invert-lang",
        "keep-alive",
        "log-dws-status",
        "use-native-window-events",
    ])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("detach", False)

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    ]
    user_agent = random.choice(user_agents)
    options.add_argument(f"--user-agent={user_agent}")

    if config.proxy:
        options.add_argument(f"--proxy-server={config.proxy}")

    driver = webdriver.Chrome(service=Service(config.driver_path), options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'connection', {
            get: function() {
                return {
                    effectiveType: '4g',
                    rtt: 50,
                    downlink: 10,
                    ping: 12,
                    saveData: false,
                    addEventListener: function() {},
                    removeEventListener: function() {},
                    dispatchEvent: function() { return true; }
                };
            },
            configurable: true,
            enumerable: true
        });
        """
    })

    driver.execute_cdp_cmd("Network.setUserAgentOverride", {
        "userAgent": user_agent,
        "platform": "Win32"
    })

    apply_stealth(driver)

    return driver
