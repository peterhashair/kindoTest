// cypress/e2e/home.cy.ts
describe("Success flow", () => {
  it("test entire success flow", () => {
    cy.visit("/"); // Visits the baseUrl defined in cypress.config.ts
    cy.contains("Welcome to Kindo Test!").should("be.visible"); // Checks for the welcome text

    cy.contains("John Smith").should("be.visible"); // Checks for the welcome text

    cy.visit("/"); // Visits the baseUrl defined in cypress.config.ts
    cy.contains("John Smith").click(); // Clicks on the element containing "John Smith"
    cy.url().should("include", "/trips");

    cy.contains("Greenwood High Field Trip").should("be.visible");

    cy.contains("Greenwood High Field Trip").click();

    cy.contains("Book Trip").should("be.visible");

    cy.contains("Add Student").should("be.visible");

    cy.contains("Add Student").click();

    cy.contains("Student Information").should("be.visible");

    cy.get("input").eq(0).type("Example name");
    cy.get("input[id='dob']").type("1989-06-23");

    cy.contains("Save").click();

    cy.contains("Book Trip").click();

    cy.contains("Name on card").should("be.visible");

    cy.get("input[id='cardName']").type("Example name");
    cy.get("input[id='cardNumber']").type("4111111111111111");
    cy.get("input[id='expiryDate']").type("12/50");
    cy.get("input[id='cvc']").type("123");

    cy.contains("pay now").click();

    // cy.contains("Payment processed successfully!").should("be.visible");
  });
});
