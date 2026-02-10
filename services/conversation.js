/**
 * Copyright 2021-present, Facebook, Inc. All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

"use strict";

const constants = require("./constants");
const GraphApi = require('./graph-api');
const Message = require('./message');
const Cache = require('./redis');

async function sendWelcomeMessage(messageId, senderPhoneNumberId, recipientPhoneNumber) {
  const sections = [
    {
      title: "Our Services",
      rows: [
        {
          id: constants.MENU_AI_AUTOMATION,
          title: "AI & Automation",
          description: "Chatbots, Document Processing"
        },
        {
          id: constants.MENU_IOT,
          title: "IoT Solutions",
          description: "Tracking, Smart Monitoring"
        },
        {
          id: constants.MENU_DEV,
          title: "Software Development",
          description: "Web, Mobile, LMS"
        },
        {
          id: constants.MENU_DEVOPS,
          title: "Infra & DevOps",
          description: "Cloud, CI/CD, Security"
        },
        {
          id: constants.MENU_CONTACT,
          title: "Get a Quote",
          description: "Talk to an Expert"
        }
      ]
    }
  ];

  await GraphApi.sendListMessage(
    messageId,
    senderPhoneNumberId,
    recipientPhoneNumber,
    "AlkenaCode Creations",
    constants.APP_WELCOME_MESSAGE,
    "Select an option to learn more",
    sections
  );
}

async function sendServiceDescription(messageId, senderPhoneNumberId, recipientPhoneNumber, text) {
  await GraphApi.sendTextMessage(
    messageId,
    senderPhoneNumberId,
    recipientPhoneNumber,
    text
  );
}

module.exports = class Conversation {
  constructor(phoneNumberId) {
    this.phoneNumberId = phoneNumberId;
  }

  static async handleMessage(senderPhoneNumberId, rawMessage) {
    const message = new Message(rawMessage);

    // If text message, check for "Hi" or similar trigger
    if (message.type === 'text') {
      const body = message.body.toLowerCase();
      if (['hi', 'hello', 'start', 'menu'].some(w => body.includes(w))) {
        await sendWelcomeMessage(message.id, senderPhoneNumberId, message.senderPhoneNumber);
        return;
      }
    }

    switch (message.type) {
      case constants.MENU_AI_AUTOMATION:
        await sendServiceDescription(
          message.id,
          senderPhoneNumberId,
          message.senderPhoneNumber,
          constants.TEXT_AI_AUTOMATION
        );
        break;
      case constants.MENU_IOT:
        await sendServiceDescription(
          message.id,
          senderPhoneNumberId,
          message.senderPhoneNumber,
          constants.TEXT_IOT_SOLUTIONS
        );
        break;
      case constants.MENU_DEV:
        await sendServiceDescription(
          message.id,
          senderPhoneNumberId,
          message.senderPhoneNumber,
          constants.TEXT_PLATFORM_DEV
        );
        break;
      case constants.MENU_DEVOPS:
        await sendServiceDescription(
          message.id,
          senderPhoneNumberId,
          message.senderPhoneNumber,
          constants.TEXT_DEVOPS_SEC
        );
        break;
      case constants.MENU_CONTACT:
        await sendServiceDescription(
          message.id,
          senderPhoneNumberId,
          message.senderPhoneNumber,
          constants.TEXT_CONTACT_US
        );
        break;
      default:
        // For unknown inputs, simple fallback or re-send menu
        await sendWelcomeMessage(message.id, senderPhoneNumberId, message.senderPhoneNumber);
        break;
    }
  }

  static async handleStatus(senderPhoneNumberId, rawStatus) {
    // Current implementation doesn't need to track status for flow control yet
    // But keeping structure for future use
    console.log(`Status update for ${senderPhoneNumberId}: ${rawStatus.status}`);
  }
};
