/**
 * Copyright 2021-present, Facebook, Inc. All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

"use strict";

module.exports = Object.freeze({
  // Expected messages from the user
  USER_START_MESSAGE: "Hi",

  // Response messages
  APP_WELCOME_MESSAGE: "Welcome to AlkenaCode Creations! 🚀\nWe classify, predict, and generate intelligence to transform your business.\n\nHow can we assist you today?",
  APP_DEFAULT_MESSAGE: "I didn't quite catch that. Please select an option from the menu below so I can guide you better.",
  
  // Menu Descriptions
  TEXT_AI_AUTOMATION: "*AI & Automation*\nWe build custom AI assistants, chatbots, and document processing systems that understand your business context.",
  TEXT_IOT_SOLUTIONS: "*IoT Solutions*\nFrom asset tracking to smart environmental monitoring, we connect your physical operations to digital insights.",
  TEXT_PLATFORM_DEV: "*Platform Development*\nWeb, Mobile, and Desktop apps. We build scalable LMS, ride-hailing platforms, and business systems.",
  TEXT_DEVOPS_SEC: "*Infrastructure & DevOps*\nSecure, scalable cloud architecture (AWS, DigitalOcean) with automated CI/CD pipelines.",
  TEXT_CONTACT_US: "*Get in Touch*\nReady to start your project? Reply with your *Name* and *Brief Idea*, or email us at info@alkenacodecreations.co.ke.",

  // Payloads / IDs (Must be consistent)
  MENU_AI_AUTOMATION: "menu_ai_automation",
  MENU_IOT: "menu_iot",
  MENU_DEV: "menu_dev",
  MENU_DEVOPS: "menu_devops",
  MENU_CONTACT: "menu_contact"
});
