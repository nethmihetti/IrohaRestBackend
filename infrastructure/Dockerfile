FROM gradle:4.3-jdk-alpine AS TEMP_BUILD_IMAGE
USER root

ENV APP_HOME=/usr/app/
WORKDIR $APP_HOME

COPY . .

RUN chmod 755 $APP_HOME

RUN ./gradlew build --stacktrace

FROM gradle:4.3-jdk-alpine
ENV ARTIFACT_NAME=RESTserver-0.0.1-SNAPSHOT.jar
ENV APP_HOME=/usr/app/
WORKDIR $APP_HOME
COPY --from=TEMP_BUILD_IMAGE $APP_HOME/build/libs/$ARTIFACT_NAME .
EXPOSE 8080


CMD ["java","-jar", "RESTserver-0.0.1-SNAPSHOT.jar"]